from typing import OrderedDict

from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Restaurant

from .schedule import ScheduleSerializer


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
        data.update({"schedules": ScheduleSerializer(schedule, many=True).data})
        return data
