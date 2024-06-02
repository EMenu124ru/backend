from django.contrib import admin

from apps.restaurants.models import TagToPlace


@admin.register(TagToPlace)
class TagToPlaceAdmin(admin.ModelAdmin):
    """Class representation of TagToPlace model in admin panel."""

    list_display = (
        "id",
        "name",
        "type",
    )
