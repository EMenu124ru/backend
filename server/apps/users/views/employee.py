from django.conf import settings
from django.middleware import csrf
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import Employee
from apps.users.permissions import FromSameRestaurantEmployee, IsCurrentUser
from apps.users.serializers import (
    EmployeeAuthSerializer,
    EmployeeScheduleSerializer,
    EmployeeSerializer,
)


class EmployeeCookieAuthAPIView(TokenObtainPairView):
    serializer_class = EmployeeAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'],
            value=serializer.validated_data["access"],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=serializer.validated_data["refresh"],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        csrf.get_token(request)
        return response


class EmployeeHeaderAuthAPIView(TokenObtainPairView):
    serializer_class = EmployeeAuthSerializer


class EmployeeRetrieveAPIView(RetrieveAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated & IsCurrentUser,)

    def get_object(self):
        return Employee.objects.get(user_id=self.request.user.id)


class EmployeeScheduleRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    permission_classes = (IsAuthenticated & FromSameRestaurantEmployee,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EmployeeScheduleSerializer(
            instance.schedule.all(),
            many=True,
        )
        return Response(serializer.data)
