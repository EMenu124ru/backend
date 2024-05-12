from django.conf import settings
from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import (
    ClientCookieAuthAPIView,
    ClientHeaderAuthAPIView,
    EmployeeCookieAuthAPIView,
    EmployeeHeaderAuthAPIView,
    EmployeeRetrieveAPIView,
    EmployeeScheduleFileCreateAPIView,
    EmployeeScheduleRetrieveAPIView,
    EmployeesKitchenRetrieveListAPIView,
    EmployeesRetrieveListAPIView,
    EmployeesUpdateListAPIView,
    TokenRefreshCookieAPIView,
)

staff_login = (
    path("staff/login", EmployeeHeaderAuthAPIView.as_view(), name="staff-login")
    if settings.DEBUG
    else path("staff/login", EmployeeCookieAuthAPIView.as_view(), name="staff-login")
)
client_login = (
    path("clients/login", ClientHeaderAuthAPIView.as_view(), name="client-login")
    if settings.DEBUG
    else path("clients/login", ClientCookieAuthAPIView.as_view(), name="client-login")
)
token_refresh = (
    path("auth/token/refresh", TokenRefreshView.as_view(), name="refresh")
    if settings.DEBUG
    else path("auth/token/refresh", TokenRefreshCookieAPIView.as_view(), name="refresh")
)

urlpatterns = [
    staff_login,
    client_login,
    token_refresh,
    path('devices', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    path("staff/me", EmployeeRetrieveAPIView.as_view(), name="staff-detail"),
    path("staff/<int:pk>/schedule", EmployeeScheduleRetrieveAPIView.as_view(), name="staff-schedule"),
    path("staff/<int:pk>", EmployeesUpdateListAPIView.as_view(), name="staff-update"),
    path("employee-schedule/file", EmployeeScheduleFileCreateAPIView.as_view(), name="staff-schedule-file"),
    path("staff/kitchen", EmployeesKitchenRetrieveListAPIView.as_view(), name="staff-kitchen"),
    path("staff", EmployeesRetrieveListAPIView.as_view(), name="staff-list"),
]
