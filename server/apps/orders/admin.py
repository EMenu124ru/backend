from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Class representation of Category model in admin panel."""

    list_display = (
        "id",
        "name",
    )


@admin.register(models.Dish)
class DishAdmin(admin.ModelAdmin):
    """Class representation of Dish model in admin panel."""

    list_display = (
        "id",
        "category",
        "name",
        "description",
        "price",
    )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Class representation of Order model in admin panel."""

    list_display = (
        "id",
        "price",
        "comment",
        "employee",
    )


@admin.register(models.DishImages)
class DishImagesAdmin(admin.ModelAdmin):
    """Class representation of DishImages model in admin panel."""

    list_display = (
        "id",
        "image",
        "dish",
    )


@admin.register(models.OrderAndDishes)
class OrderAndDishesAdmin(admin.ModelAdmin):
    """Class representation of OrderAndDishes model in admin panel."""

    list_display = (
        "id",
        "order",
        "dish",
    )


@admin.register(models.RestaurantAndOrder)
class RestaurantAndOrderAdmin(admin.ModelAdmin):
    """Class representation of RestaurantAndOrder model in admin panel."""

    list_display = (
        "id",
        "arrival_time",
        "order",
        "restaurant",
        "place_number",
    )


@admin.register(models.StopList)
class StopListAdmin(admin.ModelAdmin):
    """Class representation of StopList model in admin panel."""

    list_display = (
        "id",
    )
