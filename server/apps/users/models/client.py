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
        return (
            "Client"
            f"(id={self.pk},"
            f"user_id={self.user.pk},"
            f"user.username={self.user.username},"
            f"user.first_name={self.user.first_name},"
            f"user.last_name={self.user.last_name},"
            f"user.surname={self.user.surname},"
            f"user.phone_number={self.user.phone_number},"
            f"bonuses={self.bonuses})"
        )
