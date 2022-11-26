from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

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


class Client(models.Model):
    user = models.OneToOneField(
        User,
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


class Employee(models.Model):

    class Roles(models.TextChoices):
        """Class choices."""

        WAITER = "WAITER", "Официант"
        BARTENDER = "BARTENDER", "Бармен"
        COOK = "COOK", "Повар"
        CHEF = "CHEF", "Шеф-повар"
        MANAGER = "MANAGER", "Управляющий"
        HOSTESS = "HOSTESS", "Хостес"

    user = models.OneToOneField(
        User,
        related_name="employee",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    role = models.CharField(
        max_length=64,
        choices=Roles.choices,
        verbose_name="Роль",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="staff",
        verbose_name="Ресторан",
    )

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self) -> str:
        return f"Employee {self.user.first_name} {self.user.last_name} {self.role}"
