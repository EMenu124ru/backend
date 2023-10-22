from rest_framework import permissions

from apps.core.viewsets import CreateReadUpdateViewSet
from apps.orders.models import Reservation
from apps.orders.permissions import ReservationPermission
from apps.orders.serializers import ReservationSerializer


class ReservationViewSet(CreateReadUpdateViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (
        permissions.IsAuthenticated & ReservationPermission,
    )

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)
