from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .client import Client


class User(AbstractUser):
    surname = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default="",
        verbose_name='Отчество',
    )
    phone_number = PhoneNumberField(
        max_length=17,
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

    def __str__(self) -> str:
        return (
            "User"
            f"(id={self.pk},"
            f"username={self.username},"
            f"first_name={self.first_name},"
            f"last_name={self.last_name},"
            f"surname={self.surname},"
            f"phone_number={self.phone_number},"
            f"is_client={self.is_client})"
        )
