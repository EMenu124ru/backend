from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_arrival_time(arrival_time) -> None:
    if timezone.now() >= arrival_time:
        raise ValidationError(
            "Время прихода не может быть раньше текущего времени",
        )


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
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="reservation",
        verbose_name="Номер места",
    )

    class Meta:
        verbose_name = "Забронированный стол"
        verbose_name_plural = "Забронированные столы"

    def __str__(self) -> str:
        return f"Reservation {self.arrival_time} {self.restaurant} {self.place} {self.user}"
