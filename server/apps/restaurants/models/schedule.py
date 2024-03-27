from django.db import models


class Schedule(models.Model):
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
        return f"Schedule {self.restaurant} {self.time_start} {self.time_finish} {self.week_day}"
