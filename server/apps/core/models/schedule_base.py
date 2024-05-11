from django.db import models


class ScheduleBase(models.Model):
    class WeekDays(models.IntegerChoices):
        """Week day choices"""
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

    week_day = models.IntegerField(
        choices=WeekDays.choices,
        verbose_name="День недели",
    )
    time_start = models.TimeField(
        verbose_name="Время начала работы",
    )
    time_finish = models.TimeField(
        verbose_name="Время окончания работы",
    )

    class Meta:
        abstract = True
