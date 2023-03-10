from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_arrival_time(arrival_time) -> None:
    if timezone.now() >= arrival_time:
        raise ValidationError(
            "Время прихода не может быть раньше текущего времени",
        )


class RestaurantAndOrder(models.Model):
    arrival_time = models.DateTimeField(
        validators=[validate_arrival_time],
        verbose_name="Время прибытия",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="restaurant_and_order",
        verbose_name="Заказ",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="restaurant_and_order",
        verbose_name="Ресторан",
    )
    place_number = models.PositiveIntegerField(
        verbose_name="Номер места",
    )

    class Meta:
        verbose_name = "Ресторан и заказ"
        verbose_name_plural = "Ресторан и заказы"

    def __str__(self) -> str:
        return f"RestaurantAndOrder {self.arrival_time} {self.order} {self.restaurant}"
