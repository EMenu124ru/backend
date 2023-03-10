from rest_framework import permissions

from apps.core.viewsets import CreateUpdateDestroyViewSet
from apps.orders.models import OrderAndDish
from apps.orders.permissions import OrderAndDishPermission
from apps.orders.serializers import OrderAndDishSerializer


class OrderAndDishViewSet(CreateUpdateDestroyViewSet):
    queryset = OrderAndDish.objects.all()
    serializer_class = OrderAndDishSerializer
    permission_classes = (
        permissions.IsAuthenticated & OrderAndDishPermission,
    )
