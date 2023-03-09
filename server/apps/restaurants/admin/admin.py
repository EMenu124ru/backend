from django.contrib import admin

from ..models import models


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Class representation of Restaurant model in admin panel."""

    list_display = (
        "id",
        "address",
    )


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Class representation of Schedule model in admin panel."""

    list_display = (
        "id",
        "restaurant",
        "time_open",
        "time_close",
        "week_day",
    )
