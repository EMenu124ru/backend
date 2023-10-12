from django.urls import re_path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import EmployeeAuthAPIView, EmployeeRetrieveAPIView

urlpatterns = [
    re_path(r"staff/login/?", EmployeeAuthAPIView.as_view()),
    re_path(r"staff/(?P<pk>[0-9]+)/$", EmployeeRetrieveAPIView.as_view()),
    re_path(r"token/refresh/?", TokenRefreshView.as_view()),
]
