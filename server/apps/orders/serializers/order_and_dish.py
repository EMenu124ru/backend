from collections import OrderedDict

from apps.core.serializers import BaseSerializer, serializers
from apps.users.models import Client, Employee

from apps.orders.models import OrderAndDish, Dish, Order


class DishCommentSerializer(BaseSerializer):

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


class OrderAndDishSerializer(BaseSerializer):

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
