from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.orders.models import Order

ACCESS_STATUS = [
    Order.Statuses.WAITING_FOR_COOKING,
    Order.Statuses.COOKING,
    Order.Statuses.WAITING_FOR_DELIVERY,
    Order.Statuses.IN_PROCESS_DELIVERY,
    Order.Statuses.DELIVERED,
    Order.Statuses.PAID,
]


def get_restaurant_id(order: Order):
    employee = order.employee
    if employee and employee.restaurant_id:
        return employee.restaurant_id

    reservation = order.reservation
    if reservation and reservation.restaurant_id:
        return reservation.restaurant_id


def get_orders_by_restaurant(restaurant_id: int) -> QuerySet:
    delta = timedelta(hours=14)
    now = timezone.now()
    left_bound = now - delta
    return Order.objects.filter(
        Q(employee__restaurant_id=restaurant_id) &
        Q(status__in=ACCESS_STATUS) &
        (
            Q(created__gte=left_bound) |
            Q(reservation__arrival_time__gte=left_bound)
        )
    ).order_by("status")


def update_order_list(restaurant_id: int, orders: QuerySet | list[Order]) -> None:
    from apps.restaurants.consumers.room import Events, OrderService

    group_name = f"restaurant_{restaurant_id}"
    body = {"orders": OrderService.get_orders_list_sync(orders)}
    async_to_sync(get_channel_layer().group_send)(
        group_name,
        {
            "type": Events.LIST_ORDERS,
            "body": body,
        },
    )
