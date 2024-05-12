from django.contrib import admin

from apps.users.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Class representation of Schedule model in admin panel."""

    list_display = (
        "id",
        "employee",
        "time_start",
        "time_finish",
        "is_approve",
        "type",
        "day",
    )
