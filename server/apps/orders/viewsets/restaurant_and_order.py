from rest_framework import permissions

from apps.core.views import BaseViewSet
from apps.orders.models import RestaurantAndOrder
from apps.orders.permissions import RestaurantAndOrderPermission
from apps.orders.serializers import RestaurantAndOrderSerializer


class RestaurantAndOrderViewSet(BaseViewSet):
    queryset = RestaurantAndOrder.objects.all()
    serializer_class = RestaurantAndOrderSerializer
    permission_classes = (
        permissions.IsAuthenticated & RestaurantAndOrderPermission,
    )

    def perform_destroy(self, instance) -> None:
        if instance.order:
            instance.order.delete()
        instance.delete()
