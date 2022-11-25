from collections import Counter, OrderedDict
from decimal import Decimal

from rest_framework import serializers

from apps.core.serializers import BaseSerializer
from apps.restaurants.models import Restaurant
from apps.users.models import Client, Employee

from . import models


class CategorySerializer(BaseSerializer):

    class Meta:
        model = models.Category
        fields = (
            "id",
            "name",
        )


class DishImageSerializer(BaseSerializer):

    class Meta:
        model = models.DishImages
        fields = (
            "id",
            "image",
        )


class DishSerializer(BaseSerializer):

    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
    )

    class Meta:
        model = models.Dish
        fields = (
            "id",
            "category",
            "name",
            "description",
            "short_description",
            "price",
            "compound",
            "weight",
        )

    def to_representation(self, instance: models.Dish) -> OrderedDict:
        data = super().to_representation(instance)
        new_info = {
            "images": DishImageSerializer(instance.images.all(), many=True).data,
            "category": CategorySerializer(instance=instance.category).data,
        }
        data.update(new_info)
        return data


class OrderSerializer(BaseSerializer):

    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        allow_null=True,
        required=False,
    )
    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        allow_null=True,
        required=False,
    )
    dishes = serializers.PrimaryKeyRelatedField(
        queryset=models.Dish.objects.all(),
        many=True,
    )

    class Meta:
        model = models.Order
        fields = (
            "id",
            "status",
            "comment",
            "employee",
            "client",
            "place_number",
            "dishes",
        )

    def create(self, validated_data: OrderedDict) -> models.Order:
        dishes = validated_data.pop("dishes")
        validated_data.update(
            {"price": sum([Decimal(dish.price) for dish in dishes])}
        )
        order = models.Order.objects.create(**validated_data)
        models.OrderAndDishes.objects.bulk_create(
            [
                models.OrderAndDishes(
                    order=order,
                    dish=dish,
                )
                for dish in dishes
            ],
        )
        return order

    def check_fields_by_client(
        self,
        instance: models.Order,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("dishes", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def check_fields_by_cook(
        self,
        instance: models.Order,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("status", None)
        data.pop("comment", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def get_dishes(
        self,
        received: list[int],
        existing: list[int],
    ) -> list[list, list]:
        received, existing = Counter(received), Counter(existing)
        delete, create = [], []
        for idx, count in existing.items():
            if idx in received:
                if received[idx] < count:
                    delete.extend([idx for _ in range(count-received[idx])])
                if received[idx] > count:
                    create.extend([idx for _ in range(received[idx-count])])
            else:
                delete.extend([idx for _ in range(count)])
        for idx, count in received.items():
            if idx not in existing:
                create.extend([idx for _ in range(count)])
        return create, delete

    def update(
        self,
        instance: models.Order,
        validated_data: OrderedDict,
    ) -> models.Order:
        if (
            self._user.is_client and
            not self.check_fields_by_client(instance, validated_data)
        ):
            raise serializers.ValidationError(
                "Пользователь может изменить только состав заказа",
            )
        if not self._user.is_client:
            if (
                self._user.employee.role in (
                    Employee.Roles.CHEF,
                    Employee.Roles.COOK,
                    Employee.Roles.BARTENDER,
                ) and
                not self.check_fields_by_cook(instance, validated_data)
            ):
                raise serializers.ValidationError(
                    "Работник может изменить только статус и комментарий к заказу",
                )
        dishes = validated_data.pop("dishes", [])
        if dishes:
            existing = models.OrderAndDishes.objects.filter(
                order=instance
            ).values_list(
                "dish__id",
                flat=True,
            )
            create, delete = self.get_dishes(
                [dish.id for dish in dishes],
                existing,
            )
            models.OrderAndDishes.objects.filter(
                order=instance,
                dish__id__in=delete,
            ).delete()
            models.OrderAndDishes.objects.bulk_create(
                [
                    models.OrderAndDishes(
                        order=instance,
                        dish=dish,
                    )
                    for dish in models.Dish.objects.filter(id__in=create)
                ],
            )
            instance.price = sum([Decimal(dish.price) for dish in dishes])
            instance.save()
        return super().update(instance, validated_data)

    def validate_dishes(self, dishes) -> list:
        if not dishes:
            raise serializers.ValidationError("Заказ не может быть без блюд")
        return dishes

    def to_representation(self, instance: models.Order) -> OrderedDict:
        data = super().to_representation(instance)
        pk_dishes = instance.dishes.values_list("dish", flat=True)
        dishes = models.Dish.objects.filter(id__in=pk_dishes)
        new_info = {
            "dishes": DishSerializer(dishes, many=True).data,
            "price": instance.price,
        }
        data.update(new_info)
        return data


class RestaurantAndOrderSerializer(BaseSerializer):

    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
    )
    order = OrderSerializer(
        allow_null=True,
    )

    class Meta:
        model = models.RestaurantAndOrder
        fields = (
            "id",
            "arrival_time",
            "order",
            "restaurant",
        )

    def create(self, validated_data: OrderedDict) -> models.RestaurantAndOrder:
        order_dict = validated_data.pop("order")
        order = None
        if order_dict is not None:
            order_dict["dishes"] = [dish.id for dish in order_dict["dishes"]]
            order_dict["employee"] = self._user.employee.id
            serializer = OrderSerializer(data=order_dict)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            order = models.Order.objects.get(id=serializer.data["id"])
        restaurant_and_orders = models.RestaurantAndOrder.objects.create(
            arrival_time=validated_data["arrival_time"],
            restaurant=validated_data["restaurant"],
            order=order,
        )
        return restaurant_and_orders
