from datetime import timedelta
from zoneinfo import ZoneInfo

from django.utils import timezone

from apps.orders.models import Reservation
from config import celery_app

COUNT_HOURS = 2


@celery_app.task
def close_inactive_reservation():
    checked_reservation = Reservation.objects.filter(orders__isnull=True)
    current_time = timezone.now()

    count_canceled = 0
    for reservation in checked_reservation:
        restaurant = reservation.restaurant
        current_time = timezone.localtime(current_time, timezone=ZoneInfo(restaurant.time_zone))
        arrival_time = timezone.localtime(reservation.arrival_time, timezone=ZoneInfo(restaurant.time_zone))

        critical_time = arrival_time + timedelta(hours=COUNT_HOURS)

        if current_time >= critical_time and not reservation.orders.exists():
            reservation.status = Reservation.Statuses.CANCELED
            reservation.save()
            count_canceled += 1
    return count_canceled
