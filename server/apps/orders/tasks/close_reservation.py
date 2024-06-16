from datetime import timedelta
from zoneinfo import ZoneInfo

from django.utils import timezone

from apps.orders.models import Reservation
from apps.restaurants.models import Restaurant
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


@celery_app.task
def close_reservation_after_close_restaurant():
    restaurants = Restaurant.objects.order_by("id").prefetch_related("reservations", "schedule").all()
    need_more = False
    count_updates = 0
    for restaurant in restaurants:
        current_time = timezone.localtime(
            timezone.now(),
            timezone=ZoneInfo(restaurant.time_zone),
        ).replace(tzinfo=None)

        restaurant_schedule = restaurant.schedule.filter(
            week_day=current_time.today().weekday(),
        )
        if not restaurant_schedule.exists():
            continue

        schedule = restaurant_schedule.first()
        if schedule.time_finish > current_time.time():
            need_more = True
            continue

        opened_reservations = restaurant.reservations.filter(
            status=Reservation.Statuses.OPENED,
        )
        for reservation in opened_reservations:
            reservation.status = Reservation.Statuses.FINISHED
            reservation.save()
            count_updates += 1
    if need_more:
        close_reservation_after_close_restaurant.apply_async(countdown=200)
    return count_updates
