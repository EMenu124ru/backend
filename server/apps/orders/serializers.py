from collections import OrderedDict
from decimal import Decimal

from apps.core.serializers import BaseSerializer, serializers
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
            "dish",
            "image",
        )
        write_only_fields = (
            "dish",
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


class DishCommentSerializer(BaseSerializer):

    dish = serializers.PrimaryKeyRelatedField(
        queryset=models.Dish.objects.all(),
    )

    class Meta:
        model = models.OrderAndDishes
        fields = (
            "id",
            "dish",
            "comment",
        )


class OrderAndDishSerializer(BaseSerializer):

    dish = serializers.PrimaryKeyRelatedField(
        queryset=models.Dish.objects.all(),
    )
    order = serializers.PrimaryKeyRelatedField(
        queryset=models.Order.objects.all(),
    )
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,
    )

    class Meta:
        model = models.OrderAndDishes
        fields = (
            "id",
            "status",
            "order",
            "dish",
            "comment",
            "employee",
        )

    def check_fields_by_cook(
        self,
        instance: models.OrderAndDishes,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("status", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def check_fields_by_chef(
        self,
        instance: models.OrderAndDishes,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("employee", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def check_fields_by_sous_chef(
        self,
        instance: models.OrderAndDishes,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("employee", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def check_fields_by_waiter(
        self,
        instance: models.OrderAndDishes,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("comment", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self.instance:
            if (
                self._user.employee.role == Employee.Roles.WAITER and
                not self.check_fields_by_waiter(self.instance, attrs)
            ):
                raise serializers.ValidationError(
                    "Официант может изменить только комментарий к заказу",
                )
            if (
                self._user.employee.role == Employee.Roles.COOK and
                not self.check_fields_by_cook(self.instance, attrs)
            ):
                raise serializers.ValidationError(
                    "Повар может изменить только статус заказа",
                )
            if any([
                self._user.employee.role == Employee.Roles.CHEF and
                not self.check_fields_by_chef(self.instance, attrs),
                self._user.employee.role == Employee.Roles.SOUS_CHEF and
                not self.check_fields_by_sous_chef(self.instance, attrs)
            ]):
                raise serializers.ValidationError(
                    "Шеф и су-шеф могут менять только работника, который будет готовить блюдо",
                )
        return attrs


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
    dishes = DishCommentSerializer(
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
            "dishes",
        )

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

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self.instance:
            if (
                self._user.employee.role in (
                    Employee.Roles.CHEF,
                    Employee.Roles.COOK,
                    Employee.Roles.BARTENDER,
                ) and
                not self.check_fields_by_cook(self.instance, attrs)
            ):
                raise serializers.ValidationError(
                    "Работник может изменить только статус и комментарий к заказу",
                )
        return attrs

    def create(self, validated_data: OrderedDict) -> models.Order:
        dishes = validated_data.pop("dishes")
        validated_data.update(
            {"price": sum([Decimal(item["dish"].price) for item in dishes])}
        )
        order = models.Order.objects.create(**validated_data)
        models.OrderAndDishes.objects.bulk_create(
            [
                models.OrderAndDishes(
                    order=order,
                    dish=item["dish"],
                    comment=item.get("comment", ""),
                )
                for item in dishes
            ],
        )
        return order

    def update(
        self,
        instance: models.Order,
        validated_data: OrderedDict,
    ) -> models.Order:
        validated_data.pop("dishes", None)
        return super().update(instance, validated_data)

    def to_representation(self, instance: models.Order) -> OrderedDict:
        data = super().to_representation(instance)
        dishes = instance.dishes.values("id", "dish", "comment")
        for item in dishes:
            item["dish"] = models.Dish.objects.get(id=item["dish"])
        new_info = {
            "dishes": DishCommentSerializer(dishes, many=True).data,
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
            "place_number",
        )

    def check_fields_by_hostess(
        self,
        instance: models.RestaurantAndOrder,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("arrival_time", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self._user.is_client:
            return attrs
        if self.instance:
            if (
                self._user.employee.role == Employee.Roles.HOSTESS and
                not self.check_fields_by_hostess(self.instance, attrs)
            ):
                raise serializers.ValidationError(
                    "Редактируя бронь, хостесс может менять только время прибытия",
                )
            return attrs
        if (
            self._user.employee.role == Employee.Roles.HOSTESS and
            attrs.get("order", None) is not None
        ):
            raise serializers.ValidationError(
                "Создавая бронь, хостесс не может создать заказ",
            )
        return attrs

    def create(self, validated_data: OrderedDict) -> models.RestaurantAndOrder:
        order_dict = validated_data.pop("order")
        order = None
        if order_dict is not None:
            if self._user.is_client:
                order_dict["client"] = self._user.client.id
            else:
                order_dict["employee"] = self._user.employee.id
            for dish in order_dict["dishes"]:
                dish["dish"] = dish["dish"].id
            serializer = OrderSerializer(data=order_dict)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            order = models.Order.objects.get(id=serializer.data["id"])
        restaurant_and_orders = models.RestaurantAndOrder.objects.create(
            arrival_time=validated_data["arrival_time"],
            restaurant=validated_data["restaurant"],
            place_number=validated_data["place_number"],
            order=order,
        )
        return restaurant_and_orders


class StopListSerializer(BaseSerializer):

    dish = serializers.PrimaryKeyRelatedField(
        queryset=models.Dish.objects.all(),
    )
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = models.StopList
        fields = (
            "id",
            "dish",
            "restaurant",
        )

    def validate_dishes(self, dishes) -> list:
        if not dishes:
            raise serializers.ValidationError(
                "Нельзя создать стоп лист без блюд",
            )
        return dishes
