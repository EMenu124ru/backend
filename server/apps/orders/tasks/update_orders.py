from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from apps.orders.functions import get_restaurant_id, update_order_list_in_group
from apps.orders.models import Order, OrderAndDish
from config import celery_app

COUNT_SECONDS = 30


@celery_app.task
def send_updated_orders():
    now = timezone.now()
    left_border_first = now - timedelta(seconds=COUNT_SECONDS)
    orders = OrderAndDish.objects.filter(
        Q(created__gte=left_border_first) |
        Q(modified__gte=left_border_first)
    ).values_list("order_id", flat=True).distinct()

    restaurant_orders = set()
    for order in Order.objects.filter(id__in=set(orders)):
        restaurant_id = get_restaurant_id(order)
        restaurant_orders.add(restaurant_id)

    for restaurant_id in restaurant_orders:
        update_order_list_in_group(restaurant_id)
