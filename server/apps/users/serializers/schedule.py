from apps.core.serializers import BaseModelSerializer, serializers
from apps.users.models import Employee, Schedule


class EmployeeScheduleSerializer(BaseModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
    )

    class Meta:
        model = Schedule
        fields = (
            "id",
            "time_start",
            "time_finish",
            "employee",
            "is_approve",
            "type",
            "day",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["week_day"] = instance.day.weekday()
        return data
