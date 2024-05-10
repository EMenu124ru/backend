from rest_framework import (
    permissions,
    response,
    status,
)

from apps.core.viewsets import CreateReadUpdateViewSet
from apps.orders.models import Reservation
from apps.orders.permissions import ReservationPermission
from apps.orders.serializers import OrderSerializer, ReservationSerializer


class ReservationViewSet(CreateReadUpdateViewSet):
    serializer_class = ReservationSerializer
    permission_classes = (
        permissions.IsAuthenticated & ReservationPermission,
    )

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        order_dict = data.pop("order", None)
        reservation_serializer = self.get_serializer(data=data)
        reservation_serializer.is_valid(raise_exception=True)
        self.perform_create(reservation_serializer)
        if order_dict is not None:
            order_dict["reservation"] = reservation_serializer.instance.pk
            order_dict["client"] = request.user.client.id
            serializer = OrderSerializer(data=order_dict)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return response.Response(
            ReservationSerializer(reservation_serializer.instance).data,
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        if self.request.user.is_client:
            return Reservation.objects.filter(client=self.request.user.client)
        return Reservation.objects.filter(
            restaurant=self.request.user.employee.restaurant,
        )
