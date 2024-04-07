from datetime import timedelta

from django.db.models import F, Q
from django.utils import timezone

from apps.orders.functions import (
    ACCESS_STATUS,
    get_restaurant_id,
    update_order_list,
)
from apps.orders.models import OrderAndDish
from config import celery_app

COUNT_SECONDS = 30


@celery_app.task
def send_updated_orders():
    now = timezone.now()
    left_border_first = now - timedelta(seconds=COUNT_SECONDS)
    left_border_second = now - timedelta(hours=14)
    orders = OrderAndDish.objects.filter(
        Q(order__status__in=ACCESS_STATUS) &
        ~Q(modified=F("created")) &
        ~Q(order__modified=F("order__created")) &
        (
            Q(modified__gte=left_border_first) |
            Q(order__modified__gte=left_border_first)
        ) &
        (
            Q(created__gte=left_border_second) |
            Q(order__reservation__arrival_time__gte=left_border_second)
        )
    ).order_by("order__status").values_list("order", flat=True).distinct()

    restaurant_orders = {}
    for order in orders:
        restaurant_id = get_restaurant_id(order)
        if restaurant_id not in restaurant_orders:
            restaurant_orders[restaurant_id] = []
        restaurant_orders[restaurant_id].append(order)

    for restaurant_id, orders in restaurant_orders:
        update_order_list(restaurant_id, orders)
