from collections import OrderedDict

from apps.core.serializers import BaseModelSerializer, serializers
from apps.orders.models import Reservation
from apps.restaurants.models import (
    Place,
    Restaurant,
    TagToPlace,
)
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
    tag_to_location = serializers.PrimaryKeyRelatedField(
        queryset=TagToPlace.objects.filter(type=TagToPlace.Types.LOCATION),
        allow_null=True,
        required=False,
        write_only=True,
    )
    tag_to_number = serializers.PrimaryKeyRelatedField(
        queryset=TagToPlace.objects.filter(type=TagToPlace.Types.NUMBER_OF_SEATS),
        allow_null=True,
        required=False,
        write_only=True,
    )
    client_phone_number = serializers.CharField(
        allow_null=True,
        required=False,
        write_only=True,
    )

    class Errors:
        CLIENT_CANT_CHOOSE_PLACE = "Клиент не может выбрать или поменять место"
        CANT_UPDATE_ORDER = "Нельзя данным методом обновить заказ"
        CANT_SET_THIS_FIELD = "Нельзя установить это поле во время создания брони"
        DONT_SELECT_PLACE_TAGS = "Выберите тэги к месту"
        HASNT_FREE_PLACES = "Нет свободных мест"
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
            "client_full_name",
            "client_phone_number",
            "place",
            "comment",
            "tag_to_location",
            "tag_to_number",
        )
        editable_fields = {
            Employee.Roles.WAITER: [
                "place",
                "status",
            ],
            Employee.Roles.HOSTESS: [
                "place",
                "arrival_time",
                "status",
                "client_full_name",
            ],
        }

    def validate_client_phone_number(self, client_phone_number):
        if self.instance and client_phone_number:
            return None
        return client_phone_number

    def validate_place_instance(self, place, restaurant):
        if not restaurant.places.filter(pk=place.id).exists():
            raise serializers.ValidationError(self.Errors.PLACE_DONT_EXISTS)
        if Reservation.objects.filter(place=place, status=Reservation.Statuses.OPENED).exists():
            raise serializers.ValidationError(self.Errors.PLACE_ALREADY_BUSY)
        return place

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
        restaurant = attrs.get("restaurant")
        if self._user.is_client:
            tag_to_number, tag_to_location = attrs.pop("tag_to_number", None), attrs.pop("tag_to_location", None)

            if not (tag_to_number and tag_to_location):
                raise serializers.ValidationError(self.Errors.DONT_SELECT_PLACE_TAGS)

            free, _, _ = restaurant.get_places(",".join(map(str, [tag_to_number.pk, tag_to_location.pk])))
            if not free:
                raise serializers.ValidationError(self.Errors.HASNT_FREE_PLACES)

            for place in free:
                try:
                    attrs["place"] = self.validate_place_instance(place, restaurant)
                    print(attrs["place"])
                except serializers.ValidationError as exception:
                    print(exception)
                    continue
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
            restaurant,
        )
        return attrs

    def get_client(self, validated_data: OrderedDict):
        client_phone_number = validated_data.pop("client_phone_number", None)
        if self._user.is_client:
            return self._user.client

        validated_client = validated_data.get("client", None)
        if validated_client:
            return validated_client

        if client_phone_number:
            query = Client.objects.filter(user__phone_number__exact=client_phone_number)
            if query.exists():
                return query.first()

            client_full_name = validated_data.get("client_full_name")
            if client_full_name:
                names = client_full_name.split(" ")
                while len(names) < 3:
                    names.append("")
                first_name, last_name, surname = names
                client_data = dict(
                    first_name=first_name,
                    last_name=last_name if last_name else first_name,
                    surname=surname if surname else first_name,
                    phone_number=client_phone_number,
                )
                serializer = ClientSerializer(data=client_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return serializer.instance

        return None

    def create(self, validated_data: OrderedDict) -> Reservation:
        validated_data["client"] = self.get_client(validated_data)
        return super().create(validated_data)

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
        data["client"] = ClientSerializer(client).data if client else client
        return data
