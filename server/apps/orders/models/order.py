from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    class Statuses(models.TextChoices):
        WAITING_FOR_COOKING = "WAITING_FOR_COOKING", "Передано на кухню"
        COOKING = "COOKING", "Готовится"
        WAITING_FOR_DELIVERY = "WAITING_FOR_DELIVERY", "Ожидает доставки/готово к выдаче"
        IN_PROCESS_DELIVERY = "IN_PROCESS_DELIVERY", "В процессе доставки"
        DELIVERED = "DELIVERED", "Доставлен"
        FINISHED = "FINISHED", "Закрыт"
        CANCEL = "CANCEL", "Отменен"
        PAID = "PAID", "Оплачен"

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

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"Order {self.price} {self.comment} {self.employee}"
