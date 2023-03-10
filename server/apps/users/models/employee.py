from django.db import models


class Employee(models.Model):
    class Roles(models.TextChoices):
        """Class choices."""

        WAITER = "WAITER", "Официант"
        BARTENDER = "BARTENDER", "Бармен"
        COOK = "COOK", "Повар"
        CHEF = "CHEF", "Шеф-повар"
        SOUS_CHEF = "SOUS_CHEF", "Су-Шеф"
        MANAGER = "MANAGER", "Управляющий"
        HOSTESS = "HOSTESS", "Хостес"

    user = models.OneToOneField(
        "users.User",
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
