from typing import OrderedDict

from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Restaurant

from .place import PlaceSerializer
from .schedule import ScheduleSerializer


class RestaurantDataSerializer(BaseModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "address",
        )


class RestaurantSerializer(BaseModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "address",
        )

    def to_representation(self, instance: Restaurant) -> OrderedDict:
        data = super().to_representation(instance)
        schedule = instance.schedule.all()
        places = instance.places.all()
        info = {
            "schedules": ScheduleSerializer(schedule, many=True).data,
            "places": PlaceSerializer(places, many=True).data,
        }
        data.update(info)
        return data
