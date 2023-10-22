from collections import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import Reservation
from apps.orders.serializers import OrderSerializer
from apps.restaurants.models import Place, Restaurant
from apps.restaurants.serializers import PlaceSerializer, RestaurantSerializer
from apps.users.models import Client, Employee
from apps.users.serializers import ClientSerializer


class ReservationSerializer(BaseModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
    )
    place = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "status",
            "arrival_time",
            "restaurant",
            "client",
            "place",
        )

    def check_fields_by_waiter(
        self,
        instance: Reservation,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("place", None)
        data.pop("status", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def check_fields_by_hostess(
        self,
        instance: Reservation,
        validated_data: OrderedDict,
    ) -> bool:
        data = validated_data.copy()
        data.pop("place", None)
        data.pop("arrival_time", None)
        data.pop("status", None)
        return all([
            instance.__getattribute__(key) == value
            for key, value in data.items()
        ])

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self._user.is_client:
            if "place" in attrs:
                raise serializers.ValidationError(
                    "Клиент не может выбрать или поменять стол",
                )
            return attrs
        if self.instance:
            if self.instance.status in (
                Reservation.Statuses.CANCELED,
                Reservation.Statuses.FINISHED,
            ):
                raise serializers.ValidationError(
                    "Нельзя менять бронирование, когда оно уже завершено или отменено",
                )
            restaurant = attrs.get("restaurant", self.instance.restaurant)
            place = attrs.get("place", self.instance.place)
            if not restaurant.places.filter(pk=place.id).exists():
                raise serializers.ValidationError(
                    "Данного стола нет в ресторане",
                )
            if (
                self._user.employee.role == Employee.Roles.HOSTESS and
                not self.check_fields_by_hostess(self.instance, attrs)
            ):
                raise serializers.ValidationError(
                    "Редактируя бронь, хостес может менять только стол, время прибытия и статус",
                )
            if (
                self._user.employee.role == Employee.Roles.WAITER and
                not self.check_fields_by_waiter(self.instance, attrs)
            ):
                raise serializers.ValidationError(
                    "Редактируя бронь, официант может менять только стол и статус",
                )
            return attrs
        restaurant = attrs.get("restaurant")
        place = attrs.get("place")
        if not restaurant.places.filter(pk=place.id).exists():
            raise serializers.ValidationError(
                "Данного стола нет в ресторане",
            )
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        restaurant = Restaurant.objects.get(pk=data["restaurant"])
        data["restaurant"] = RestaurantSerializer(restaurant).data

        if (place_id := data.pop("place", None)) is not None:
            place = Place.objects.get(pk=place_id)
            data["place"] = PlaceSerializer(place).data

        client = None
        if (client_id := data.pop("client", None)) is not None:
            client = Client.objects.get(pk=client_id)

        data["client"] = ClientSerializer(client).data
        data["orders"] = OrderSerializer(instance.orders.all(), many=True).data
        return data
