from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import Employee
from apps.users.permissions import IsCurrentUser
from apps.users.serializers import EmployeeAuthSerializer, EmployeeSerializer


class EmployeeAuthAPIView(TokenObtainPairView):
    serializer_class = EmployeeAuthSerializer


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsCurrentUser,)
