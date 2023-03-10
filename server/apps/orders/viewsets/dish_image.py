from rest_framework import permissions

from apps.core.views import DestroyViewSet
from apps.orders.models import DishImage
from apps.orders.permissions import DishPermission


class DishImageViewSet(DestroyViewSet):
    queryset = DishImage.objects.all()
    permission_classes = (
        permissions.IsAuthenticated & DishPermission,
    )
