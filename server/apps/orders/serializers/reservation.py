from collections import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import Reservation
from apps.restaurants.models import (
    Place,
    Restaurant,
    TagToPlace,
)
from apps.restaurants.serializers import (
    PlaceSerializer,
    RestaurantSerializer,
    TagToPlaceSerializer,
)
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
    tag_to_place = serializers.PrimaryKeyRelatedField(
        queryset=TagToPlace.objects.all(),
        allow_null=True,
        required=False,
    )

    class Errors:
        CLIENT_CANT_CHOOSE_PLACE = "Клиент не может выбрать или поменять место"
        CANT_SET_THIS_FIELD = "Нельзя установить это поле во время создания брони"
        CANT_UPDATE_ORDER = "Нельзя данным методом обновить заказ"
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
            "count_quests",
            "tag_to_place",
        )
        editable_fields = {
            Employee.Roles.WAITER: ["place", "status"],
            Employee.Roles.HOSTESS: ["place", "arrival_time", "status", "tag_to_place", "count_quests"],
        }

    def validate_place_instance(self, place, restaurant):
        if not restaurant.places.filter(pk=place.id).exists():
            raise serializers.ValidationError(self.Errors.PLACE_DONT_EXISTS)
        if Reservation.objects.filter(place=place, status=Reservation.Statuses.OPENED).exists():
            raise serializers.ValidationError(self.Errors.PLACE_ALREADY_BUSY)

    def validate_status(self, status: Reservation.Statuses) -> Reservation.Statuses:
        if not self.instance and status:
            raise serializers.ValidationError(self.Errors.CANT_SET_THIS_FIELD)
        if self.instance and self.instance.status in (
            Reservation.Statuses.CANCELED,
            Reservation.Statuses.FINISHED,
        ):
            raise serializers.ValidationError(self.Errors.RESTORE_CLOSED_RESERVATION)
        return status

    def validate_order(self, order):
        if self.instance and order:
            raise serializers.ValidationError(self.Errors.CANT_UPDATE_ORDER)
        return order

    def validate_place(self, place: Place) -> Place:
        if self._user.is_client and place:
            raise serializers.ValidationError(self.Errors.CLIENT_CANT_CHOOSE_PLACE)
        return place

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if self._user.is_client:
            return attrs
        if self.instance:
            self.validate_place_instance(
                attrs.get("place", self.instance.place),
                attrs.get("restaurant", self.instance.restaurant),
            )
            role = self._user.employee.role
            if (
                role == Employee.Roles.HOSTESS and
                not self.check_fields(role, attrs.copy())
            ):
                raise serializers.ValidationError(self.Errors.HOSTESS_CHANGES)
            if (
                role == Employee.Roles.WAITER and
                not self.check_fields(role, attrs.copy())
            ):
                raise serializers.ValidationError(self.Errors.WAITER_CHANGES)
            return attrs
        self.validate_place_instance(
            attrs.get("place"),
            attrs.get("restaurant"),
        )
        return attrs

    def create(self, validated_data: OrderedDict) -> Reservation:
        client = None
        if self._user.is_client:
            client = self._user.client
        validated_data["client"] = client
        return super().create(validated_data)

    def to_representation(self, instance):
        from .order import OrderSerializer

        data = super().to_representation(instance)
        restaurant = Restaurant.objects.get(pk=data["restaurant"])
        data["restaurant"] = RestaurantSerializer(restaurant).data

        if (place_id := data.pop("place", None)) is not None:
            place = Place.objects.get(pk=place_id)
            data["place"] = PlaceSerializer(place).data

        if (tag_to_place_id := data.pop("tag_to_place", None)) is not None:
            tag_to_place = TagToPlace.objects.get(pk=tag_to_place_id)
            data["tag_to_place"] = TagToPlaceSerializer(tag_to_place).data

        client = None
        if (client_id := data.pop("client", None)) is not None:
            client = Client.objects.get(pk=client_id)

        data["orders"] = OrderSerializer(instance.orders.all(), many=True).data
        data["client"] = ClientSerializer(client).data
        return data
