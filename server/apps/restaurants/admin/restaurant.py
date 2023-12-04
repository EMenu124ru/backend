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
        return obj.schedule.all()

    def get_places(self, obj):
        return [place.place for place in obj.places.all()]
