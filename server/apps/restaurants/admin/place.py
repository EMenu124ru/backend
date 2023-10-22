from django.contrib import admin

from apps.restaurants.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Class representation of Place model in admin panel."""

    list_display = (
        "id",
        "restaurant",
        "place",
    )
