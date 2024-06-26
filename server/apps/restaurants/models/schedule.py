from django.db import models

from apps.core.models import ScheduleBase


class Schedule(ScheduleBase):
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
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="schedule",
        verbose_name="Ресторан",
    )

    class Meta:
        verbose_name = "Расписание работы ресторана"
        verbose_name_plural = "Расписания работы ресторанов"
        unique_together = ("week_day", "restaurant")

    def __str__(self) -> str:
        return (
            "Schedule"
            f"(id={self.pk},"
            f"restaurant_id={self.restaurant.pk},"
            f"week_day={self.week_day},"
            f"time_start={self.time_start},"
            f"time_finish={self.time_finish})"
        )
