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
        "get_place",
        "comment",
    )

    def get_place(self, obj):
        if obj.place:
            return obj.place.place
        return obj.place
