from django.db import models


class Schedule(models.Model):
    class Types(models.TextChoices):
        WORK = "WORK", "Рабочая смена"
        SICK_LEAVE = "SICK_LEAVE", "Больничный"
        VACATION = "VACATION", "Отпуск"
        DAY_OFF = "DAY_OFF", "Выходной"

    time_start = models.DateTimeField(
        verbose_name="Время начала работы",
    )
    time_finish = models.DateTimeField(
        verbose_name="Время окончания работы",
    )
    employee = models.ForeignKey(
        "users.Employee",
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name="Сотрудник",
    )
    is_approve = models.BooleanField(
        default=True,
        verbose_name="Подтверждение менеджера",
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
        return f"Schedule {self.employee} {self.type} {self.time_start} {self.time_finish}"
