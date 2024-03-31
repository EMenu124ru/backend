from collections import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import (
    Dish,
    Order,
    OrderAndDish,
)
from apps.orders.serializers import DishSerializer
from apps.users.models import Employee
from apps.users.serializers import EmployeeSerializer


class BaseOrderAndDishSerializer(BaseModelSerializer):

    dish = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(),
    )

    class Meta:
        model = OrderAndDish
        fields = (
            "id",
            "dish",
            "count",
            "comment",
        )


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

    class Errors:
        WAITER_CHANGES = "Официант может изменить только количество блюд в заказе и статус"
        COOK_CHANGES = "Повар может изменить только статус заказа"
        CHEF_CHANGES = (
            "Шеф и су-шеф могут изменять только работника, "
            "который будет готовить блюдо, и статус"
        )
        SET_CANCELED_STATUS = "Если блюдо нужно убрать из заказа, то поставьте статус отменен"
        VALID_COUNT_DISHES = "Введите корректное значение для обозначения количества блюд в заказе"

    class Meta:
        model = OrderAndDish
        fields = (
            "id",
            "status",
            "order",
            "dish",
            "count",
            "employee",
            "comment",
        )

    def check_fields_by_chef(
        self,
        instance: OrderAndDish,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("employee", None)
        data.pop("status", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

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

    def check_fields_by_waiter(
        self,
        instance: OrderAndDish,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("count", None)
        data.pop("comment", None)
        data.pop("status", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def validate_count(self, count: int) -> int:
        exception_text = self.Errors.VALID_COUNT_DISHES
        if self.instance:
            exception_text = self.Errors.SET_CANCELED_STATUS
        if count <= 0:
            raise serializers.ValidationError(exception_text)
        return count

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self.instance:
            if (
                self._user.employee.role == Employee.Roles.WAITER and
                not self.check_fields_by_waiter(self.instance, attrs)
            ):
                raise serializers.ValidationError(self.Errors.WAITER_CHANGES)
            if (
                self._user.employee.role == Employee.Roles.COOK and
                not self.check_fields_by_cook(self.instance, attrs)
            ):
                raise serializers.ValidationError(self.Errors.COOK_CHANGES)
            if (
                self._user.employee.role in (
                    Employee.Roles.CHEF,
                    Employee.Roles.SOUS_CHEF,
                ) and not self.check_fields_by_chef(self.instance, attrs)
            ):
                raise serializers.ValidationError(self.Errors.CHEF_CHANGES)
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
