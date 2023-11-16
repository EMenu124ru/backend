from rest_framework import (
    generics,
    permissions,
    response,
)
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import Employee
from apps.users.permissions import FromSameRestaurantEmployee, IsCurrentUser
from apps.users.serializers import (
    EmployeeAuthSerializer,
    EmployeeScheduleSerializer,
    EmployeeSerializer,
)


class EmployeeAuthAPIView(TokenObtainPairView):
    serializer_class = EmployeeAuthSerializer


class EmployeeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated & IsCurrentUser,)

    def get_object(self):
        return Employee.objects.get(user_id=self.request.user.id)


class EmployeeScheduleRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    permission_classes = (permissions.IsAuthenticated & FromSameRestaurantEmployee,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EmployeeScheduleSerializer(
            instance.schedule.all(),
            many=True,
        )
        return response.Response(serializer.data)
