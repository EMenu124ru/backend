from django.contrib import admin

from apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Class representation of Review model in admin panel."""

    list_display = (
        "id",
        "review",
        "mark",
        "client",
    )
