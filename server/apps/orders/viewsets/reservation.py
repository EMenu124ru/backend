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

        if self.request.user.is_client:
            data["client"] = self.request.user.client.pk
        else:
            data["restaurant"] = self.request.user.employee.restaurant.pk

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

    def perform_create(self, serializer):
        if self.request.user.is_client:
            serializer.save(client=self.request.user.client)
        else:
            serializer.save(restaurant=self.request.user.employee.restaurant)

    def get_queryset(self):
        reservation = Reservation.objects.all()
        if self.request.user.is_client:
            reservation = reservation.filter(
                client=self.request.user.client,
            )
        else:
            reservation = reservation.filter(
                restaurant=self.request.user.employee.restaurant,
            )
        return reservation.order_by("arrival_time")
