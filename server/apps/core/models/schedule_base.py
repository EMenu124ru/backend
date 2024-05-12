from django.db import models


class ScheduleBase(models.Model):
    time_start = models.TimeField(
        verbose_name="Время начала работы",
    )
    time_finish = models.TimeField(
        verbose_name="Время окончания работы",
    )

    class Meta:
        abstract = True
