from django.contrib import admin

from apps.restaurants.models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Class representation of Plan model in admin panel."""

    list_display = (
        "id",
        "plan",
    )
