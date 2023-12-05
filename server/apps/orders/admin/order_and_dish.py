from django.contrib import admin

from apps.orders.models import OrderAndDish


@admin.register(OrderAndDish)
class OrderAndDishAdmin(admin.ModelAdmin):
    """Class representation of OrderAndDish model in admin panel."""

    list_display = (
        "id",
        "order",
        "dish",
        "status",
        "employee",
        "count",
    )
