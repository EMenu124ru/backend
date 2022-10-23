from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.orders.viewsets import CategoryViewSet, DishViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("dishes", DishViewSet, basename="dishes")

app_name = "api"
urlpatterns = router.urls
