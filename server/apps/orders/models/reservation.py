from django.core import exceptions, validators
from django.db import models
from django.utils import timezone

from apps.orders.constants import OrderErrors


def validate_arrival_time(arrival_time) -> None:
    if timezone.now() >= arrival_time:
        raise exceptions.ValidationError(OrderErrors.WRONG_ARRIVAL_TIME)


class Reservation(models.Model):
    class Statuses(models.TextChoices):
        OPENED = "OPENED", "Открыт"
        FINISHED = "FINISHED", "Закрыт"
        CANCELED = "CANCELED", "Отменен"

    status = models.TextField(
        choices=Statuses.choices,
        default=Statuses.OPENED,
        verbose_name="Статус бронирования",
    )
    arrival_time = models.DateTimeField(
        validators=[validate_arrival_time],
        verbose_name="Время прибытия",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Ресторан",
    )
    client = models.ForeignKey(
        "users.Client",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reservations",
        verbose_name="Клиент",
    )
    place = models.ForeignKey(
        "restaurants.Place",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reservations",
        verbose_name="Номер места",
    )
    count_guests = models.PositiveIntegerField(
        default=1,
        validators=[validators.MinValueValidator(1)],
        verbose_name="Количество гостей",
    )
    tag_to_place = models.ForeignKey(
        "restaurants.TagToPlace",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Тэг к месту",
    )
    comment = models.TextField(
        default="",
        blank=True,
        verbose_name="Комментарий",
    )

    class Meta:
        verbose_name = "Забронированный стол"
        verbose_name_plural = "Забронированные столы"

    def __str__(self) -> str:
        return (
            "Reservation"
            f"(id={self.pk},"
            f"arrival_time={self.arrival_time},"
            f"status={self.status},"
            f"comment={self.comment},"
            f"count_guests={self.count_guests},"
            f"restaurant_id={self.restaurant.pk},"
            f"place={self.place},"
            f"tag_to_place={self.tag_to_place},"
            f"client={self.client})"
        )
