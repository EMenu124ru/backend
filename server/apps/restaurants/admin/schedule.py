from django.contrib import admin

from apps.restaurants.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Class representation of Schedule model in admin panel."""

    list_display = (
        "id",
        "restaurant",
        "time_start",
        "time_finish",
        "week_day",
    )
