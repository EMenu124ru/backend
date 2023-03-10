from rest_framework import permissions

from apps.core.viewsets import BaseViewSet
from apps.orders.models import Order
from apps.orders.permissions import OrderPermission
from apps.orders.serializers import OrderSerializer


class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (
        permissions.IsAuthenticated & OrderPermission,
    )

    def perform_create(self, serializer) -> None:
        serializer.save(employee=self.request.user.employee)
