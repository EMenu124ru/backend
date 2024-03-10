from django.db import models

from apps.core.models import ObjectFile


class Employee(models.Model):
    class Roles(models.TextChoices):
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
    education = models.TextField(
        default="",
        blank=True,
        verbose_name="Образование",
    )
    place_of_birth = models.TextField(
        default="",
        blank=True,
        verbose_name="Место рождения",
    )
    citizenship = models.TextField(
        default="",
        blank=True,
        verbose_name="Гражданство",
    )
    personnel_number = models.PositiveIntegerField(
        verbose_name="Табельный номер",
    )
    medical_checkup = models.DateField(
        default="",
        blank=True,
        null=True,
        verbose_name="Медицинский осмотр",
    )
    employment_contract = models.TextField(
        default="",
        blank=True,
        verbose_name="Трудовой договор",
    )
    work_experience = models.TextField(
        default="",
        blank=True,
        verbose_name="Стаж работы",
    )
    image = models.ForeignKey(
        "core.ObjectFile",
        default=ObjectFile.create_default_object,
        on_delete=models.CASCADE,
        verbose_name="Фото сотрудника",
    )

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self) -> str:
        return f"Employee {self.user.first_name} {self.user.last_name} {self.role}"
