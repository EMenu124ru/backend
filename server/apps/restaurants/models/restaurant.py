import zoneinfo

from django.conf import settings
from django.db import models

from apps.orders.models import Reservation

AVAILABLE_TIMEZONES = sorted([
    (zone, zone)
    for zone in zoneinfo.available_timezones()
    if "Asia" in zone or "Europe" in zone
])


class Restaurant(models.Model):
    address = models.TextField(
        verbose_name="Адрес",
    )
    timezone = models.CharField(
        choices=AVAILABLE_TIMEZONES,
        default=settings.TIME_ZONE,
        max_length=20,
        verbose_name="Временная зона"
    )

    def get_places(self, tags: str) -> tuple[list, list, list]:
        places = self.places.all()
        if tags:
            places = places.filter(tags__in=tags.split(",")).order_by("id").distinct()
        free, reserved, busy = [], [], []
        free_statuses = [
            Reservation.Statuses.CANCELED,
            Reservation.Statuses.FINISHED,
        ]
        for place in places:
            reservations = place.reservations.all()

            opened = reservations.filter(status=Reservation.Statuses.OPENED)
            if opened.filter(orders__isnull=True):
                reserved.append(place)
                continue

            if opened.filter(orders__isnull=False):
                busy.append(place)
                continue

            if not reservations or reservations.filter(status__in=free_statuses):
                free.append(place)
                continue
        return free, reserved, busy

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

    def __str__(self) -> str:
        return (
            "Restaurant"
            f"(id={self.pk},"
            f"timezone={self.timezone},"
            f"address={self.address})"
        )
