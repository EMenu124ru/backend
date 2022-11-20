from decimal import Decimal

from rest_framework import serializers

from apps.restaurants.models import Restaurant
from apps.users.models import Client, Employee

from . import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            "id",
            "name",
        )


class DishImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DishImages
        fields = (
            "id",
            "image",
        )


class DishSerializer(serializers.ModelSerializer):

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        new_info = {
            "images": DishImageSerializer(instance.images.all(), many=True).data,
            "category": CategorySerializer(instance=instance.category).data,
        }
        data.update(new_info)
        return data


class OrderSerializer(serializers.ModelSerializer):

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

    def create(self, validated_data) -> models.Order:
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

    def update(self, instance, validated_data) -> models.Order:
        dishes = validated_data.pop("dishes")
        if dishes:
            models.OrderAndDishes.objects.filter(order=instance).delete()
            models.OrderAndDishes.objects.bulk_create(
                [
                    models.OrderAndDishes(
                        order=instance,
                        dish=dish,
                    )
                    for dish in dishes
                ],
            )
            instance.price = sum([Decimal(dish.price) for dish in dishes])
            instance.save()
        return super().update(instance, validated_data)

    def validate_dishes(self, dishes) -> list:
        if not dishes:
            raise serializers.ValidationError("Заказ не может быть без блюд")
        return dishes

    def to_representation(self, instance):
        data = super().to_representation(instance)
        pk_dishes = instance.dishes.values_list("dish", flat=True)
        dishes = models.Dish.objects.filter(id__in=pk_dishes)
        new_info = {
            "dishes": DishSerializer(dishes, many=True).data,
            "price": instance.price,
        }
        data.update(new_info)
        return data


class RestaurantAndOrderSerializer(serializers.ModelSerializer):

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

    def create(self, validated_data) -> models.RestaurantAndOrder:
        order_dict = validated_data.pop("order")
        order = None
        if order_dict is not None:
            order_dict["dishes"] = [dish.id for dish in order_dict["dishes"]]
            order_dict["employee"] = self.context["request"].user.employee.id
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
