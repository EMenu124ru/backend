from django.contrib.auth.models import AbstractUser
from django.db import models

from .client import Client


class User(AbstractUser):
    surname = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Отчество',
        default="",
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
            f'{self.username}, '
            f'is_client {self.is_client}'
        )
