from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import EmployeeAuthAPIView

urlpatterns = [
    path("staff/login/", EmployeeAuthAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
