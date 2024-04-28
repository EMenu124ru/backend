from rest_framework import permissions

from apps.core.viewsets import CreateReadUpdateViewSet
from apps.orders.functions import get_orders_by_restaurant
from apps.orders.permissions import OrderPermission
from apps.orders.serializers import OrderSerializer


class OrderViewSet(CreateReadUpdateViewSet):
    serializer_class = OrderSerializer
    permission_classes = (
        permissions.IsAuthenticated & OrderPermission,
    )

    def get_queryset(self):
        return get_orders_by_restaurant(
            self.request.user.employee.restaurant_id,
            self.request.user.employee.role,
        )

    def perform_create(self, serializer) -> None:
        serializer.save(employee=self.request.user.employee)
