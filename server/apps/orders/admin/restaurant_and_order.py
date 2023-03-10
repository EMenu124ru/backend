from django.contrib import admin

from apps.orders.models import RestaurantAndOrder


@admin.register(RestaurantAndOrder)
class RestaurantAndOrderAdmin(admin.ModelAdmin):
    """Class representation of RestaurantAndOrder model in admin panel."""

    list_display = (
        "id",
        "arrival_time",
        "order",
        "restaurant",
        "place_number",
    )
