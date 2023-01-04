from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.orders.viewsets import (
    CategoryViewSet,
    DishImageViewSet,
    DishViewSet,
    OrderAndDishesViewSet,
    OrderViewSet,
    RestaurantAndOrderViewSet,
    StopListViewSet,
)
from apps.users.viewsets import ClientViewSet

router = (DefaultRouter if settings.DEBUG else SimpleRouter)(
    trailing_slash=False
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
    "restaurant-and-orders",
    RestaurantAndOrderViewSet,
    basename="restaurantAndOrders",
)
router.register(
    "order-and-dishes",
    OrderAndDishesViewSet,
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

app_name = "api"
urlpatterns = router.urls
