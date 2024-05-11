from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .client import Client

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Телефонный номер должен быть введен в формате: '+999999999'",
)


class User(AbstractUser):
    surname = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Отчество',
        default="",
    )
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex],
        unique=True,
        verbose_name="Телефонный номер",
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения",
    )
    address = models.TextField(
        default="",
        blank=True,
        verbose_name="Адрес проживания",
    )

    @property
    def is_client(self) -> bool:
        try:
            return self.client is not None
        except Client.DoesNotExist:
            return False

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def str(self) -> str:
        return (
            "User"
            f"(username={self.username},"
            f"first_name={self.first_name},"
            f"last_name={self.last_name},"
            f"surname={self.surname},"
            f"is_client={self.is_client})"
        )
