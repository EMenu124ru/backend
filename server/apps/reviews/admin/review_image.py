from django.contrib import admin

from apps.reviews.models import ReviewImage


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    """Class representation of ReviewImage model in admin panel."""

    list_display = (
        "id",
        "image",
        "review",
    )
