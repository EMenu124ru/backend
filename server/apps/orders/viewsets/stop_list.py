from apps.core.viewsets import CreateReadDestroyViewSet
from apps.orders.models import StopList
from apps.orders.permissions import StopListPermission
from apps.orders.serializers import StopListSerializer


class StopListViewSet(CreateReadDestroyViewSet):
    serializer_class = StopListSerializer
    permission_classes = (StopListPermission,)

    def get_queryset(self):
        queryset = StopList.objects.all()
        if self.action == "list":
            return queryset.filter(
                restaurant=self.request.user.employee.restaurant,
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.employee.restaurant)
