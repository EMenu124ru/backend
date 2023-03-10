from django.contrib import admin

from apps.orders.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Class representation of Category model in admin panel."""

    list_display = (
        "id",
        "name",
    )
