from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.orders.viewsets import (
    CategoryViewSet,
    DishImageViewSet,
    DishViewSet,
    OrderAndDishViewSet,
    OrderViewSet,
    RestaurantAndOrderViewSet,
    StopListViewSet,
)
from apps.reviews.viewsets import ReviewImageViewSet, ReviewViewSet
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
    OrderAndDishViewSet,
    basename="orderAndDishes",
)
router.register(
    "stop-list",
    StopListViewSet,
    basename="stopList",
)
router.register(
    "reviews",
    ReviewViewSet,
    basename="reviews",
)
router.register(
    "review-images",
    ReviewImageViewSet,
    basename="review-images",
)
router.register(
    "clients",
    ClientViewSet,
    basename="clients",
)

app_name = "api"
urlpatterns = [
    path("", include("apps.users.urls")),
] + router.urls
