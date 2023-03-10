from django.core.validators import RegexValidator
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
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефонный номер должен быть введен в формате: '+999999999'",
    )
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex],
        unique=True,
        verbose_name="Телефонный номер",
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self) -> str:
        return f"Client {self.user.first_name} {self.user.last_name} {self.phone_number}"
