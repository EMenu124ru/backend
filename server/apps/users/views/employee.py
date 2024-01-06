from django.conf import settings
from django.middleware import csrf
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import Employee
from apps.users.permissions import (
    FromSameRestaurantEmployee,
    IsChef,
    IsCurrentUser,
    IsManager,
)
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
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            domain=request.get_host(),
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=serializer.validated_data["refresh"],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            domain=request.get_host(),
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
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


class EmployeesKitchenRetrieveListAPIView(ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated & IsChef,)

    def get_queryset(self):
        available_role = [
            Employee.Roles.CHEF,
            Employee.Roles.COOK,
            Employee.Roles.SOUS_CHEF,
        ]
        return Employee.objects.filter(
            restaurant=self.request.user.employee.restaurant.id,
            role__in=available_role,
        ).order_by("role")


class EmployeesRetrieveListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated & IsManager,)

    def get_queryset(self):
        return Employee.objects.filter(
            restaurant=self.request.user.employee.restaurant.id,
        )

    def get(self, request, *args, **kwargs):
        employees_by_roles = {}
        employees = self.get_queryset()
        for employee in employees:
            if employee.role not in employees_by_roles:
                employees_by_roles[employee.role] = []
            employees_by_roles[employee.role].append(EmployeeSerializer(employee).data)
        return Response(employees_by_roles, status=status.HTTP_200_OK)


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
