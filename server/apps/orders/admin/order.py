from django.contrib import admin

from apps.orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Class representation of Order model in admin panel."""

    list_display = (
        "id",
        "status",
        "comment",
        "price",
        "comment",
        "employee",
        "reservation",
    )
