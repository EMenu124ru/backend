from django.contrib import admin

from apps.orders.models import StopList


@admin.register(StopList)
class StopListAdmin(admin.ModelAdmin):
    """Class representation of StopList model in admin panel."""

    list_display = (
        "id",
        "ingredient",
        "restaurant",
        "created_at",
    )
