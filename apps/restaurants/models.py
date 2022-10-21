from django.db import models


class Restaurant(models.Model):
    address = models.TextField(
        verbose_name="Адрес",
    )

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

    def __str__(self) -> str:
        return f"Restaurant {self.address}"


class Schedule(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Ресторан",
    )
    time_open = models.DateTimeField(
        verbose_name="Время открытия",
    )
    time_close = models.DateTimeField(
        verbose_name="Время закрытия",
    )

    class WeekDays(models.IntegerChoices):
        """Week day choices"""
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    week_day = models.IntegerField(
        choices=WeekDays.choices,
        verbose_name="День недели",
    )

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"

    def __str__(self) -> str:
        return f"Schedule {self.restaurant} {self.time_open} {self.time_close} {self.week_day}"
