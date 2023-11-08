from django.db import models

from apps.core.models import ScheduleBase


class Schedule(ScheduleBase):
    day = models.DateField(
        verbose_name="Дата",
    )
    employee = models.ForeignKey(
        "users.Employee",
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name="Сотрудник",
    )

    class Meta:
        verbose_name = "Расписание работы сотрудника"
        verbose_name_plural = "Расписания работы сотрудника"

    def __str__(self) -> str:
        return f"Schedule {self.employee} {self.time_start} {self.time_finish} {self.day}"
