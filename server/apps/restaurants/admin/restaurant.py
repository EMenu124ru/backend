from django.contrib import admin

from apps.restaurants.models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Class representation of Restaurant model in admin panel."""

    list_display = (
        "id",
        "address",
    )
