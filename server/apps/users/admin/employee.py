from django.contrib import admin

from apps.users.models import Employee


@admin.register(Employee)
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

    @admin.display(empty_value='???')
    def surname(self, obj):
        return obj.user.surname
