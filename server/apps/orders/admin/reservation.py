from django.contrib import admin

from apps.orders.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Class representation of Reservation model in admin panel."""

    list_display = (
        "id",
        "status",
        "arrival_time",
        "restaurant",
        "client",
        "place",
        "comment",
    )
