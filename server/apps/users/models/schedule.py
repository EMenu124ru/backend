from django.db import models

from apps.core.models import ScheduleBase


class Schedule(ScheduleBase):
    class Types(models.TextChoices):
        WORK = "WORK", "Рабочая смена"
        SICK_LEAVE = "SICK_LEAVE", "Больничный"
        VACATION = "VACATION", "Отпуск"
        DAY_OFF = "DAY_OFF", "Выходной"

    day = models.DateField(
        verbose_name="Дата",
    )
    employee = models.ForeignKey(
        "users.Employee",
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name="Сотрудник",
    )
    type = models.CharField(
        max_length=64,
        choices=Types.choices,
        default=Types.WORK,
        verbose_name="Тип элемента расписания",
    )

    class Meta:
        verbose_name = "Расписание работы сотрудника"
        verbose_name_plural = "Расписания работы сотрудника"

    def __str__(self) -> str:
        return f"Schedule {self.employee} {self.type} {self.day} {self.time_start} {self.time_finish}"
