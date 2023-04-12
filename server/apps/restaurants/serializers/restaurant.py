from typing import OrderedDict

from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Restaurant

from .plan import PlanSerializer
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
        plans = instance.plans.all()
        schedules = instance.schedules.all()
        if plans:
            data.update({"plans": PlanSerializer(plans, many=True).data})
        data.update({"schedules": ScheduleSerializer(schedules, many=True).data})
        return data
