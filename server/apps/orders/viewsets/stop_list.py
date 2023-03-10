from rest_framework import permissions

from apps.core.viewsets import CreateReadDestroyViewSet
from apps.orders.models import StopList
from apps.orders.permissions import StopListPermission
from apps.orders.serializers import StopListSerializer


class StopListViewSet(CreateReadDestroyViewSet):
    serializer_class = StopListSerializer
    permission_classes = (
        permissions.IsAuthenticated & StopListPermission,
    )

    def get_queryset(self):
        if self.action == "list":
            return StopList.objects.filter(
                restaurant=self.request.user.employee.restaurant,
            )
        return StopList.objects.all()