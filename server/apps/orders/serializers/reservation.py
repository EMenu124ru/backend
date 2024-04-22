from collections import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.functions import check_fields
from apps.orders.models import Reservation
from apps.restaurants.models import Place, Restaurant
from apps.restaurants.serializers import PlaceSerializer, RestaurantSerializer
from apps.users.models import Client, Employee
from apps.users.serializers import ClientSerializer


class ReservationSerializer(BaseModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
    )
    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        allow_null=True,
        required=False,
    )
    place = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(),
        allow_null=True,
        required=False,
    )

    class Errors:
        CLIENT_CANT_CHOOSE_PLACE = "Клиент не может выбрать или поменять место"
        RESTORE_CLOSED_RESERVATION = (
            "Нельзя менять бронирование, когда оно уже завершено или отменено"
        )
        PLACE_DONT_EXISTS = "Данного места нет в ресторане"
        PLACE_ALREADY_BUSY = "Данное место занято"
        HOSTESS_CHANGES = (
            "Редактируя бронь, хостес может менять только стол, "
            "время прибытия и статус"
        )
        WAITER_CHANGES = "Редактируя бронь, официант может менять только стол и статус"

    class Meta:
        model = Reservation
        fields = (
            "id",
            "status",
            "arrival_time",
            "restaurant",
            "client",
            "place",
            "comment",
        )

    def validate_place_instance(self, place, restaurant):
        if not restaurant.places.filter(pk=place.id).exists():
            raise serializers.ValidationError(self.Errors.PLACE_DONT_EXISTS)
        if Reservation.objects.filter(place=place, status=Reservation.Statuses.OPENED).exists():
            raise serializers.ValidationError(self.Errors.PLACE_ALREADY_BUSY)

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self._user.is_client:
            if "place" in attrs:
                raise serializers.ValidationError(self.Errors.CLIENT_CANT_CHOOSE_PLACE)
            return attrs
        if self.instance:
            if self.instance.status in (
                Reservation.Statuses.CANCELED,
                Reservation.Statuses.FINISHED,
            ):
                raise serializers.ValidationError(self.Errors.RESTORE_CLOSED_RESERVATION)
            self.validate_place_instance(
                attrs.get("place", self.instance.place),
                attrs.get("restaurant", self.instance.restaurant),
            )
            if (
                self._user.employee.role == Employee.Roles.HOSTESS and
                not check_fields(self.instance, ["place", "arrival_time", "status"], attrs)
            ):
                raise serializers.ValidationError(self.Errors.HOSTESS_CHANGES)
            if (
                self._user.employee.role == Employee.Roles.WAITER and
                not check_fields(self.instance, ["place", "status"], attrs.copy())
            ):
                raise serializers.ValidationError(self.Errors.WAITER_CHANGES)
            return attrs
        self.validate_place_instance(
            attrs.get("place"),
            attrs.get("restaurant"),
        )
        return attrs

    def to_representation(self, instance):
        from .order import OrderSerializer

        data = super().to_representation(instance)
        restaurant = Restaurant.objects.get(pk=data["restaurant"])
        data["restaurant"] = RestaurantSerializer(restaurant).data

        if (place_id := data.pop("place", None)) is not None:
            place = Place.objects.get(pk=place_id)
            data["place"] = PlaceSerializer(place).data

        client = None
        if (client_id := data.pop("client", None)) is not None:
            client = Client.objects.get(pk=client_id)

        data["orders"] = OrderSerializer(instance.orders.all(), many=True).data
        data["client"] = ClientSerializer(client).data
        return data

    def create(self, validated_data: OrderedDict) -> Reservation:
        client = None
        if self._user.is_client:
            client = self._user.client
        validated_data["client"] = client
        return super().create(validated_data)
