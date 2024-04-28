from django.db import models
from django.utils import timezone

from apps.core.models import ObjectFile

from .schedule import Schedule


class Employee(models.Model):
    class Roles(models.TextChoices):
        WAITER = "WAITER", "Официант"
        COOK = "COOK", "Повар"
        CHEF = "CHEF", "Шеф-повар"
        SOUS_CHEF = "SOUS_CHEF", "Су-Шеф"
        MANAGER = "MANAGER", "Управляющий"
        HOSTESS = "HOSTESS", "Хостес"

    class Statuses(models.TextChoices):
        ON_WORK_SHIFT_FROM_TO = "ON_WORK_SHIFT_FROM_TO", "На смене с {} до {}"
        DAY_OFF = "DAY_OFF", "Выходной"
        WILL_BE_ON_WORK_SHIFT_FROM_TO = "WILL_BE_ON_WORK_SHIFT_FROM_TO", "Будет на смене с {} до {}"
        SICK_LEAVE = "SICK_LEAVE", "Больничный"
        VACATION = "VACATION", "Отпуск"
        NOT_ON_WORK_SHIFT = "NOT_ON_WORK_SHIFT", "Не на смене"

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
        related_name="employees",
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

    def get_status(self):
        datetime_format = "%d.%m.%Y %H:%M"
        current_time = timezone.now()
        schedule = Schedule.objects.filter(
            models.Q(employee=self) &
            (
                models.Q(time_start__date=current_time.date()) |
                models.Q(time_finish__date=current_time.date())
            )
        )
        mapping_statuses = {
            Schedule.Types.DAY_OFF: Employee.Statuses.DAY_OFF,
            Schedule.Types.SICK_LEAVE: Employee.Statuses.SICK_LEAVE,
            Schedule.Types.VACATION: Employee.Statuses.VACATION,
        }
        status = Employee.Statuses.NOT_ON_WORK_SHIFT.label
        if schedule.exists():
            schedule = schedule.first()
            if schedule.is_approve:
                if schedule.type in mapping_statuses:
                    status = mapping_statuses[schedule.type].label
                else:
                    times = (
                        schedule.time_start.strftime(datetime_format),
                        schedule.time_finish.strftime(datetime_format),
                    )
                    if current_time < schedule.time_start:
                        status = Employee.Statuses.WILL_BE_ON_WORK_SHIFT_FROM_TO.label
                    else:
                        status = Employee.Statuses.ON_WORK_SHIFT_FROM_TO.label
                    status = status.format(*times)
        return status

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self) -> str:
        return f"Employee {self.user.first_name} {self.user.last_name} {self.role}"
