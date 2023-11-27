from django.contrib import admin

from apps.orders.models import Dish, DishImage, Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Class representation of Ingredient model in admin panel."""

    list_display = (
        "id",
        "name",
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Class representation of Dish model in admin panel."""

    list_display = (
        "id",
        "category",
        "name",
        "description",
        "price",
    )


@admin.register(DishImage)
class DishImageAdmin(admin.ModelAdmin):
    """Class representation of DishImage model in admin panel."""

    list_display = (
        "id",
        "image",
        "dish",
    )
