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


@admin.register(models.RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    """Class representation of RestaurantReview model in admin panel."""

    list_display = (
        "id",
        "restaurant",
        "review",
    )


@admin.register(models.DishReview)
class DishReviewAdmin(admin.ModelAdmin):
    """Class representation of DishReview model in admin panel."""

    list_display = (
        "id",
        "dish",
        "review",
    )
