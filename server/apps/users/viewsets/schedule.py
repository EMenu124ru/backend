from rest_framework import permissions

from apps.core.viewsets import CreateUpdateDestroyViewSet
from apps.users import models, serializers
from apps.users.permissions import FromSameRestaurantSchedule


class EmployeeScheduleAPIView(CreateUpdateDestroyViewSet):
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.EmployeeScheduleSerializer
    permission_classes = (permissions.IsAuthenticated & FromSameRestaurantSchedule,)
