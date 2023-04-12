from apps.core.serializers import BaseModelSerializer
from apps.restaurants.models import Schedule


class ScheduleSerializer(BaseModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "id",
            "week_day",
            "time_open",
            "time_close",
        )
