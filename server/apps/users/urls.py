from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import (
    EmployeeAuthAPIView,
    EmployeeRetrieveAPIView,
    EmployeeScheduleRetrieveAPIView,
)

urlpatterns = [
    path("staff/login", EmployeeAuthAPIView.as_view()),
    path("staff/me", EmployeeRetrieveAPIView.as_view(), name="staff-detail"),
    path("staff/<int:pk>/schedule", EmployeeScheduleRetrieveAPIView.as_view(), name="staff-schedule"),
    path("auth/token/refresh", TokenRefreshView.as_view()),
]
