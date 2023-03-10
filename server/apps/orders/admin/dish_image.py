from django.contrib import admin

from apps.orders.models import DishImage


@admin.register(DishImage)
class DishImageAdmin(admin.ModelAdmin):
    """Class representation of DishImage model in admin panel."""

    list_display = (
        "id",
        "image",
        "dish",
    )
