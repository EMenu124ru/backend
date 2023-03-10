from collections import OrderedDict
from decimal import Decimal

from apps.core.serializers import BaseSerializer, serializers
from apps.users.models import Client, Employee
from apps.orders.models import OrderAndDish, Dish, Order
from .order_and_dish import DishCommentSerializer


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
        model = Order
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
        instance: Order,
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
                ) and not self.check_fields_by_cook(self.instance, attrs)
            ):
                raise serializers.ValidationError(
                    "Работник может изменить только статус и комментарий к заказу",
                )
        return attrs

    def create(self, validated_data: OrderedDict) -> Order:
        dishes = validated_data.pop("dishes")
        validated_data.update(
            {"price": sum([Decimal(item["dish"].price) for item in dishes])}
        )
        order = Order.objects.create(**validated_data)
        OrderAndDish.objects.bulk_create(
            [
                OrderAndDish(
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
        instance: Order,
        validated_data: OrderedDict,
    ) -> Order:
        validated_data.pop("dishes", None)
        return super().update(instance, validated_data)

    def to_representation(self, instance: Order) -> OrderedDict:
        data = super().to_representation(instance)
        dishes = instance.dishes.values("id", "dish", "comment")
        for item in dishes:
            item["dish"] = Dish.objects.get(id=item["dish"])
        new_info = {
            "dishes": DishCommentSerializer(dishes, many=True).data,
            "price": instance.price,
        }
        data.update(new_info)
        return data
