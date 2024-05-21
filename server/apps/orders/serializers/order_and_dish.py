from collections import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import (
    Dish,
    Order,
    OrderAndDish,
)
from apps.orders.serializers import DishSerializer
from apps.users.models import Employee
from apps.users.serializers import EmployeeOrderSerializer


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
        WAITER_CHANGES = "Официант может изменить только количество блюд в заказе, статус и комментарий"
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
            "employee",
            "count",
            "comment",
            "created",
            "modified",
        )
        read_only_fields = (
            "created",
            "modified",
        )
        editable_fields = {
            Employee.Roles.COOK: ["status"],
            Employee.Roles.WAITER: ["count", "comment", "status"],
            Employee.Roles.SOUS_CHEF: ["employee", "status"],
            Employee.Roles.CHEF: ["employee", "status"],
        }

    def validate_count(self, count: int) -> int:
        exception_text = self.Errors.VALID_COUNT_DISHES
        if self.instance:
            exception_text = self.Errors.SET_CANCELED_STATUS
        if count <= 0:
            raise serializers.ValidationError(exception_text)
        return count

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self.instance:
            role = self._user.employee.role
            if (
                role == Employee.Roles.WAITER and
                not self.check_fields(role, attrs.copy())
            ):
                raise serializers.ValidationError(self.Errors.WAITER_CHANGES)
            if (
                role == Employee.Roles.COOK and
                not self.check_fields(role, attrs.copy())
            ):
                raise serializers.ValidationError(self.Errors.COOK_CHANGES)
            if (
                role in (
                    Employee.Roles.CHEF,
                    Employee.Roles.SOUS_CHEF,
                ) and not self.check_fields(role, attrs.copy())
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
            "employee":  None if not employee else EmployeeOrderSerializer(employee).data,
        }
        data.update(new_info)
        return data
