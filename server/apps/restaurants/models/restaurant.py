import zoneinfo
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.orders.models import Reservation

from .tag_to_place import TagToPlace

AVAILABLE_TIMEZONES = sorted([
    (zone, zone)
    for zone in zoneinfo.available_timezones()
    if "Asia" in zone or "Europe" in zone
])


class Restaurant(models.Model):
    address = models.TextField(
        verbose_name="Адрес",
    )
    time_zone = models.CharField(
        choices=AVAILABLE_TIMEZONES,
        default=settings.TIME_ZONE,
        max_length=20,
        verbose_name="Временная зона"
    )

    def get_places(self, tags: str, current_time: timezone = timezone.now()) -> tuple[list, list, list]:
        places = self.places.all()
        if tags:
            tags_instances = TagToPlace.objects.filter(id__in=tags.split(","))
            locations, number_of_seats = (
                tags_instances.filter(type=TagToPlace.Types.LOCATION),
                tags_instances.filter(type=TagToPlace.Types.NUMBER_OF_SEATS),
            )
            places = places.filter(
                models.Q(tags__in=locations) | models.Q(tags__in=number_of_seats)
            ).order_by("id").distinct()

        free, reserved, busy = [], [], []
        difference = timedelta(hours=2)

        time_zone = zoneinfo.ZoneInfo(self.time_zone)

        for place in places:
            reservations = place.reservations.filter(
                status=Reservation.Statuses.OPENED,
                arrival_time__date=current_time.date(),
            ).order_by("arrival_time")

            if not reservations.exists():
                free.append(place)
                continue

            reservation = reservations.first()
            arrival_time = timezone.localtime(
                reservation.arrival_time,
                timezone=time_zone,
            ).replace(tzinfo=None)

            arrival_time_left, arrival_time_right = arrival_time - difference, arrival_time + difference
            if arrival_time < current_time <= arrival_time_right or reservation.orders.exists():
                place.current_reservation = reservation.pk
                place.client_name = reservation.client_full_name
                busy.append(place)
                continue

            if arrival_time_left < current_time <= arrival_time and not reservation.orders.exists():
                place.current_reservation = reservation.pk
                place.client_name = reservation.client_full_name
                reserved.append(place)
                continue

        return free, reserved, busy

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

    def __str__(self) -> str:
        return (
            "Restaurant"
            f"(id={self.pk},"
            f"timezone={self.time_zone},"
            f"address={self.address})"
        )
