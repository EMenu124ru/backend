from collections import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import Order, RestaurantAndOrder
from apps.restaurants.models import Restaurant
from apps.users.models import Employee

from .order import OrderSerializer


class RestaurantAndOrderSerializer(BaseModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
    )
    order = OrderSerializer(
        allow_null=True,
    )

    class Meta:
        model = RestaurantAndOrder
        fields = (
            "id",
            "arrival_time",
            "order",
            "restaurant",
            "place_number",
        )

    def check_fields_by_hostess(
        self,
        instance: RestaurantAndOrder,
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

    def create(self, validated_data: OrderedDict) -> RestaurantAndOrder:
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
            order = Order.objects.get(id=serializer.data["id"])
        restaurant_and_orders = RestaurantAndOrder.objects.create(
            arrival_time=validated_data["arrival_time"],
            restaurant=validated_data["restaurant"],
            place_number=validated_data["place_number"],
            order=order,
        )
        return restaurant_and_orders
