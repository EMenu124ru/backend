from apps.core.serializers import BaseModelSerializer, serializers
from apps.users.models import Employee, Schedule


class EmployeeScheduleSerializer(BaseModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Schedule
        fields = (
            "id",
            "time_start",
            "time_finish",
            "employee",
            "day",
        )
