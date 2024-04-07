from datetime import timedelta

from django.utils import timezone

from apps.orders.models import Order
from config import celery_app

COUNT_HOURS = 2


@celery_app.task
def check_delayed_orders():
    now = timezone.now()
    right_border = now + timedelta(hours=COUNT_HOURS)
    Order.objects.filter(
        status=Order.Statuses.DELAYED,
        reservation__arrival_time__lte=right_border,
    ).update(status=Order.Statuses.WAITING_FOR_COOKING)
