from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.orders.viewsets import (
    CategoryViewSet,
    DishImageViewSet,
    DishViewSet,
    OrderAndDishViewSet,
    OrderViewSet,
    ReservationViewSet,
    StopListViewSet,
)
from apps.users.viewsets import ClientViewSet, EmployeeScheduleAPIView

router = (DefaultRouter if settings.DEBUG else SimpleRouter)(
    trailing_slash=False,
)
router.register(
    "categories",
    CategoryViewSet,
    basename="categories",
)
router.register(
    "dishes",
    DishViewSet,
    basename="dishes",
)
router.register(
    "orders",
    OrderViewSet,
    basename="orders",
)
router.register(
    "dish-images",
    DishImageViewSet,
    basename="dish-images",
)
router.register(
    "reservations",
    ReservationViewSet,
    basename="reservations",
)
router.register(
    "order-and-dishes",
    OrderAndDishViewSet,
    basename="orderAndDishes",
)
router.register(
    "stop-list",
    StopListViewSet,
    basename="stopList",
)
router.register(
    "clients",
    ClientViewSet,
    basename="clients",
)
router.register(
    "employee-schedule",
    EmployeeScheduleAPIView,
    basename="employeeSchedule",
)

app_name = "api"
urlpatterns = [
    path("", include("apps.users.urls")),
    path("restaurants/", include("apps.restaurants.urls")),
] + router.urls
