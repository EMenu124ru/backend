from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import BaseModel


class Order(BaseModel):
    class Statuses(models.TextChoices):
        DELAYED = "DELAYED", "Отложен"
        WAITING_FOR_COOKING = "WAITING_FOR_COOKING", "Передан на кухню"
        COOKING = "COOKING", "Готовится"
        WAITING_FOR_DELIVERY = "WAITING_FOR_DELIVERY", "Ожидает доставки/готов к выдаче"
        IN_PROCESS_DELIVERY = "IN_PROCESS_DELIVERY", "В процессе доставки"
        DELIVERED = "DELIVERED", "Доставлен/Выдан"
        PAID = "PAID", "Оплачен"
        FINISHED = "FINISHED", "Закрыт"
        CANCELED = "CANCELED", "Отменен"

    status = models.TextField(
        choices=Statuses.choices,
        default=Statuses.WAITING_FOR_COOKING,
        verbose_name="Статус заказа",
    )
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена",
    )
    comment = models.TextField(
        default="",
        blank=True,
        verbose_name="Комментарий",
    )
    employee = models.ForeignKey(
        "users.Employee",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name="Сотрудник",
    )
    client = models.ForeignKey(
        "users.Client",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name="Клиент",
    )
    reservation = models.ForeignKey(
        "orders.Reservation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="orders",
        verbose_name="Бронирование",
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return (
            "Order"
            f"(id={self.pk},"
            f"status={self.status},"
            f"price={self.price},"
            f"comment={self.comment},"
            f"employee={self.employee},"
            f"client={self.client},"
            f"modified={self.modified},"
            f"created={self.created},"
            f"reservation={self.reservation})"
        )
