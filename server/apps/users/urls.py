from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.EmployeeAuthAPIView.as_view()),
]
