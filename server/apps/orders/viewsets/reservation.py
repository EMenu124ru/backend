from rest_framework import permissions

from apps.core.viewsets import CreateReadUpdateViewSet
from apps.orders.models import Reservation
from apps.orders.permissions import ReservationPermission
from apps.orders.serializers import ReservationSerializer


class ReservationViewSet(CreateReadUpdateViewSet):
    serializer_class = ReservationSerializer
    permission_classes = (
        permissions.IsAuthenticated & ReservationPermission,
    )

    def get_queryset(self):
        if self.request.user.is_client:
            return Reservation.objects.filter(client=self.request.user.client)
        return Reservation.objects.filter(
            restaurant=self.request.user.employee.restaurant,
        )
