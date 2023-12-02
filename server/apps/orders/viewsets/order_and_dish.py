from rest_framework import permissions

from apps.core.viewsets import CreateReadUpdateViewSet
from apps.orders.models import OrderAndDish
from apps.orders.permissions import OrderAndDishPermission
from apps.orders.serializers import OrderAndDishSerializer


class OrderAndDishViewSet(CreateReadUpdateViewSet):
    serializer_class = OrderAndDishSerializer
    permission_classes = (
        permissions.IsAuthenticated & OrderAndDishPermission,
    )

    def get_queryset(self):
        return OrderAndDish.objects.filter(
            order__employee__restaurant_id=self.request.user.employee.restaurant_id,
        )
