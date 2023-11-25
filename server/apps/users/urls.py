from django.conf import settings
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import (
    ClientCookieAuthAPIView,
    ClientHeaderAuthAPIView,
    EmployeeCookieAuthAPIView,
    EmployeeHeaderAuthAPIView,
    EmployeeRetrieveAPIView,
    EmployeeScheduleRetrieveAPIView,
)

staff_login = (
    path("staff/login", EmployeeHeaderAuthAPIView.as_view())
    if settings.DEBUG
    else path("staff/login", EmployeeCookieAuthAPIView.as_view())
)
client_login = (
    path("clients/login", ClientHeaderAuthAPIView.as_view())
    if settings.DEBUG
    else path("clients/login", ClientCookieAuthAPIView.as_view())
)

urlpatterns = [
    staff_login,
    client_login,
    path("staff/me", EmployeeRetrieveAPIView.as_view(), name="staff-detail"),
    path("staff/<int:pk>/schedule", EmployeeScheduleRetrieveAPIView.as_view(), name="staff-schedule"),
    path("auth/token/refresh", TokenRefreshView.as_view()),
]
