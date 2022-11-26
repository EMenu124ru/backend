from django.db import models


class Restaurant(models.Model):
    address = models.TextField(
        verbose_name="Адрес",
    )
    reviews = models.ManyToManyField(
        "reviews.Review",
        related_name="restaurant",
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

    def __str__(self) -> str:
        return f"Restaurant {self.address}"


class Schedule(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Ресторан",
    )
    time_open = models.TimeField(
        verbose_name="Время открытия",
    )
    time_close = models.TimeField(
        verbose_name="Время закрытия",
    )

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

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"

    def __str__(self) -> str:
        return f"Schedule {self.restaurant} {self.time_open} {self.time_close} {self.week_day}"
