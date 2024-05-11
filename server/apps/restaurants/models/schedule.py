from django.db import models

from apps.core.models import ScheduleBase


class Schedule(ScheduleBase):
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
