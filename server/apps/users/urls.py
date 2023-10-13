from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import EmployeeAuthAPIView, EmployeeRetrieveAPIView

urlpatterns = [
    path("staff/login", EmployeeAuthAPIView.as_view()),
    path("staff/me", EmployeeRetrieveAPIView.as_view()),
    path("auth/token/refresh", TokenRefreshView.as_view()),
]
