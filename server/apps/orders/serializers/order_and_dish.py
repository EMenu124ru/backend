from collections import OrderedDict

from django.shortcuts import get_object_or_404

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import Dish, Order, OrderAndDish
from apps.orders.serializers import DishSerializer
from apps.users.models import Employee
from apps.users.serializers import EmployeeSerializer


class DishCommentSerializer(BaseModelSerializer):

    dish = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
    )

    class Meta:
        model = OrderAndDish
        fields = (
            "id",
            "dish",
            "comment",
        )

    def to_representation(self, instance: Order) -> OrderedDict:
        data = super().to_representation(instance)
        dish_id = data.pop("dish")
        dish = get_object_or_404(Dish, id=dish_id)
        new_info = {
            "dish": DishSerializer(dish).data,
        }
        data.update(new_info)
        return data


class OrderAndDishSerializer(BaseModelSerializer):

    dish = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
    )
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
    )
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,
    )

    class Meta:
        model = OrderAndDish
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
        instance: OrderAndDish,
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
        instance: OrderAndDish,
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
        instance: OrderAndDish,
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
        instance: OrderAndDish,
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

    def to_representation(self, instance: Order) -> OrderedDict:
        data = super().to_representation(instance)
        dish = Dish.objects.get(pk=data.pop("dish"))
        employee = None

        if (employee_id := data.pop("employee")) is not None:
            employee = Employee.objects.get(pk=employee_id)

        new_info = {
            "dish": DishSerializer(dish).data,
            "employee":  None if not employee else EmployeeSerializer(employee).data,
        }
        data.update(new_info)
        return data
