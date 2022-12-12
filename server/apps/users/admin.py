from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

admin.site.register(models.User, UserAdmin)


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    """Class representation of Client model in admin panel."""

    list_display = (
        "id",
        "first_name",
        "last_name",
        "bonuses",
        "phone_number",
    )
    autocomplete_fields = (
        "user",
    )

    @admin.display(empty_value='???')
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(empty_value='???')
    def last_name(self, obj):
        return obj.user.last_name


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Class representation of Employee model in admin panel."""

    list_display = (
        "id",
        "first_name",
        "last_name",
        "role",
    )
    autocomplete_fields = (
        "user",
    )

    @admin.display(empty_value='???')
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(empty_value='???')
    def last_name(self, obj):
        return obj.user.last_name
