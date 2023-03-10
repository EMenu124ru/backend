from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import EmployeeAuthSerializer


class EmployeeAuthAPIView(TokenObtainPairView):
    serializer_class = EmployeeAuthSerializer
