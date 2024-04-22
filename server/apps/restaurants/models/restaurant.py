from django.db import models

from apps.orders.models import Reservation


class Restaurant(models.Model):
    address = models.TextField(
        verbose_name="Адрес",
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
        return f"Restaurant {self.address}"
