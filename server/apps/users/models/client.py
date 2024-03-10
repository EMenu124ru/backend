from django.db import models


class Client(models.Model):
    user = models.OneToOneField(
        "users.User",
        related_name="client",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    bonuses = models.PositiveIntegerField(
        verbose_name="Бонусы",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self) -> str:
        return f"Client {self.user.first_name} {self.user.last_name} {self.user.phone_number}"
