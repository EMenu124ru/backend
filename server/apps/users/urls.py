from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import views

urlpatterns = [
    path("login/", views.EmployeeAuthAPIView.as_view()),
    path('', TokenRefreshView.as_view()),
]
