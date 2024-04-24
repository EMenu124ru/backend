from django.db import models
from django.core.validators import MinValueValidator

from apps.core.models import BaseModel


class OrderAndDish(BaseModel):
    class Statuses(models.TextChoices):
        WAITING_FOR_COOKING = "WAITING_FOR_COOKING", "Ожидает готовки"
        COOKING = "COOKING", "Готовится"
        DONE = "DONE", "Готов"
        CANCELED = "CANCELED", "Отменен"
        DELIVERED = "DELIVERED", "Выдан"

    status = models.TextField(
        choices=Statuses.choices,
        default=Statuses.WAITING_FOR_COOKING,
        verbose_name="Статус блюда",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="Заказ",
    )
    dish = models.ForeignKey(
        "orders.Dish",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Блюдо",
    )
    employee = models.ForeignKey(
        "users.Employee",
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="dishes",
        verbose_name="Исполняющий сотрудник",
    )
    count = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество блюд в заказе",
        validators=[MinValueValidator(1)],
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий",
    )

    class Meta:
        verbose_name = "Заказ и блюдо"
        verbose_name_plural = "Заказы и блюда"

    def __str__(self) -> str:
        return f"OrderAndDish {self.order} {self.dish}"

    def save(self, **kwargs):
        if self.pk:
            field_name = "employee"
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            if hasattr(old, field_name) and hasattr(self, field_name):
                old_value = getattr(old, field_name)
                new_value = getattr(self, field_name)
                if old_value is None and old_value != new_value:
                    self.status = OrderAndDish.Statuses.COOKING
                elif new_value is None and old_value != new_value:
                    self.status = OrderAndDish.Statuses.WAITING_FOR_COOKING
        super().save(**kwargs)
