from django.contrib import admin

from . import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    """Class representation of Client model in admin panel."""

    list_display = (
        "id",
        "bonuses",
        "phone_number",
    )
    autocomplete_fields = (
        "user",
    )


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Class representation of Employee model in admin panel."""

    list_display = (
        "id",
        "role",
    )
    autocomplete_fields = (
        "user",
    )
