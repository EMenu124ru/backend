from django.contrib import admin

from apps.orders.models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Class representation of Dish model in admin panel."""

    list_display = (
        "id",
        "category",
        "name",
        "description",
        "price",
    )
