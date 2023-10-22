from rest_framework import permissions

from apps.core.viewsets import CreateReadUpdateViewSet
from apps.orders.models import OrderAndDish
from apps.orders.permissions import OrderAndDishPermission
from apps.orders.serializers import OrderAndDishSerializer


class OrderAndDishViewSet(CreateReadUpdateViewSet):
    queryset = OrderAndDish.objects.all()
    serializer_class = OrderAndDishSerializer
    permission_classes = (
        permissions.IsAuthenticated & OrderAndDishPermission,
    )
