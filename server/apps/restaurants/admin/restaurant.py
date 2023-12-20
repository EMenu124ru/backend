from django.contrib import admin

from apps.restaurants.models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Class representation of Restaurant model in admin panel."""

    list_display = (
        "id",
        "address",
        "get_schedule",
        "get_places",
    )

    def get_schedule(self, obj):
        return ", ".join(
            map(
                lambda x: f"{x[2]}: {x[0]}-{x[1]}",
                obj.schedule.all().values_list("time_start", "time_finish", "week_day")
            )
        )

    def get_places(self, obj):
        return ", ".join(obj.places.all().values_list("place", flat=True))
