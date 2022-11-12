from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers


class EmployeeAuthAPIView(TokenObtainPairView):

    serializer_class = serializers.EmployeeAuthSerializer
