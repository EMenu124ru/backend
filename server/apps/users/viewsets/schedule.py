from rest_framework import permissions, response, status

from apps.core.viewsets import CreateUpdateDestroyViewSet
from apps.users import functions, models, serializers
from apps.users.permissions import FromSameRestaurantSchedule


class EmployeeScheduleAPIView(CreateUpdateDestroyViewSet):
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.EmployeeScheduleSerializer
    permission_classes = (permissions.IsAuthenticated & FromSameRestaurantSchedule,)

    def create(self, request, *args, **kwargs):
        data = functions.import_schedule(request)
        if 'file' not in data:
            return response.Response(
                data=data,
                status=status.HTTP_201_CREATED,
            )
        return response.Response(
            data=data,
            status=status.HTTP_400_BAD_REQUEST,
            exception=True,
        )
