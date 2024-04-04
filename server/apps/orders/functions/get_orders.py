from datetime import timedelta

from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.orders.models import Order


def get_orders_by_restaurant(restaurant_id: int) -> QuerySet:
    delta = timedelta(hours=14)
    now = timezone.now()
    left_bound = now - delta
    access_status = [
        Order.Statuses.WAITING_FOR_COOKING,
        Order.Statuses.COOKING,
        Order.Statuses.WAITING_FOR_DELIVERY,
        Order.Statuses.IN_PROCESS_DELIVERY,
        Order.Statuses.DELIVERED,
        Order.Statuses.PAID,
    ]
    return Order.objects.filter(
        Q(employee__restaurant_id=restaurant_id) &
        Q(status__in=access_status) & (
            Q(created__gte=left_bound) |
            Q(reservation__arrival_time__gte=left_bound)
        )
    ).order_by("status")
