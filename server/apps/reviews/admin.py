from django.contrib import admin

from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Class representation of Review model in admin panel."""

    list_display = (
        "id",
        "review",
        "mark",
        "client",
    )


@admin.register(models.ReviewImages)
class ReviewImagesAdmin(admin.ModelAdmin):
    """Class representation of ReviewImages model in admin panel."""

    list_display = (
        "id",
        "image",
        "review",
    )
