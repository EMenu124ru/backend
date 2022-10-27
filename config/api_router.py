from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.orders.viewsets import (
    CategoryViewSet,
    DishImageViewSet,
    DishViewSet,
    OrderViewSet,
    RestaurantAndOrderViewSet,
)

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("dishes", DishViewSet, basename="dishes")
router.register("orders", OrderViewSet, basename="orders")
router.register("dish-images", DishImageViewSet, basename="dish-images")
router.register("reservations", RestaurantAndOrderViewSet, basename="reservations")

app_name = "api"
urlpatterns = router.urls
