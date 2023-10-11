from django.conf import settings
from django.urls import include, re_path
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

router = (DefaultRouter if settings.DEBUG else SimpleRouter)()
router.register(
    r"categories/?",
    CategoryViewSet,
    basename="categories",
)
router.register(
    r"dishes/?",
    DishViewSet,
    basename="dishes",
)
router.register(
    r"orders/?",
    OrderViewSet,
    basename="orders",
)
router.register(
    r"dish-images/?",
    DishImageViewSet,
    basename="dish-images",
)
router.register(
    r"restaurant-and-orders/?",
    RestaurantAndOrderViewSet,
    basename="restaurantAndOrders",
)
router.register(
    r"order-and-dishes/?",
    OrderAndDishViewSet,
    basename="orderAndDishes",
)
router.register(
    r"stop-list/?",
    StopListViewSet,
    basename="stopList",
)
router.register(
    r"reviews/?",
    ReviewViewSet,
    basename="reviews",
)
router.register(
    r"review-images/?",
    ReviewImageViewSet,
    basename="review-images",
)
router.register(
    r"clients/?",
    ClientViewSet,
    basename="clients",
)

app_name = "api"
urlpatterns = [
    re_path("", include("apps.users.urls")),
    re_path(r"restaurants/?", include("apps.restaurants.urls")),
] + router.urls
