from collections import OrderedDict
from decimal import Decimal

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import (
    Order,
    OrderAndDish,
    Reservation,
    StopList,
)
from apps.users.models import Client, Employee
from apps.users.serializers import ClientSerializer, EmployeeSerializer

from .order_and_dish import DishCommentSerializer, OrderAndDishSerializer


class OrderSerializer(BaseModelSerializer):
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
    reservation = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(),
        allow_null=True,
        required=False,
    )
    dishes = DishCommentSerializer(
        many=True,
    )

    class Errors:
        EMPLOYEE_CHANGES = "Работник может изменить только статус и комментарий к заказу"
        INVALID_DISH = "Ингредиент в блюде {} находится в стоп листе"

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "comment",
            "employee",
            "client",
            "dishes",
            "reservation",
            "created",
            "modified",
        )
        extra_kwargs = {
            'created': {'read_only': True},
            'modified': {'read_only': True},
        }

    def check_fields_by_waiter(
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

    def get_restaurant_id(self, attrs: OrderedDict) -> int:
        if attrs.get("reservation") is not None:
            return attrs["reservation"].restaurant.pk
        return self._user.employee.restaurant.id

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self.instance:
            if (
                self._user.employee.role == Employee.Roles.WAITER and
                not self.check_fields_by_waiter(self.instance, attrs)
            ):
                raise serializers.ValidationError(self.Errors.EMPLOYEE_CHANGES)
        if attrs.get("dishes") is not None:
            order_dishes = [item["dish"] for item in attrs["dishes"]]
            restaurant_id = self.get_restaurant_id(attrs)
            for dish in order_dishes:
                ingredients_id = dish.ingredients.all().values_list('id', flat=True)
                stop_list = StopList.objects.filter(
                    ingredient_id__in=ingredients_id,
                    restaurant_id=restaurant_id,
                ).exists()
                if stop_list:
                    raise serializers.ValidationError(self.Errors.INVALID_DISH.format(dish.name))
        return attrs

    def create(self, validated_data: OrderedDict) -> Order:
        dishes = validated_data.pop("dishes")
        validated_data.update(
            {"price": sum([Decimal(item["dish"].price) for item in dishes])}
        )
        order = Order.objects.create(**validated_data)
        order_and_dishes = []
        for item in dishes:
            order_and_dish = {
                "order": order.pk,
                "dish": item["dish"].pk,
                "comment": item.get("comment", ""),
            }
            serializer = OrderAndDishSerializer(data=order_and_dish)
            serializer.is_valid(raise_exception=True)
            order_and_dishes.append(serializer)
        for item in order_and_dishes:
            item.save()
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
        employee, client = None, None
        if (employee_id := data.pop("employee")) is not None:
            employee = Employee.objects.get(pk=employee_id)

        if (client_id := data.pop("client")) is not None:
            client = Client.objects.get(pk=client_id)

        order_and_dishes = OrderAndDish.objects.filter(order_id=instance.id)
        new_info = {
            "dishes": OrderAndDishSerializer(order_and_dishes, many=True).data,
            "price": instance.price,
            "employee":  None if not employee else EmployeeSerializer(employee).data,
            "client": None if not client else ClientSerializer(client).data,
            "reservation": instance.reservation.pk if instance.reservation else None,
        }
        data.update(new_info)
        return data
