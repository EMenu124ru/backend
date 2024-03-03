from django.contrib import admin

from apps.restaurants.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Class representation of Place model in admin panel."""

    list_display = (
        "id",
        "restaurant",
        "place",
        "get_tags",
    )
    filter_horizontal = (
        "tags",
    )

    def get_tags(self, obj):
        return ", ".join(obj.tags.all().values_list("name", flat=True))
