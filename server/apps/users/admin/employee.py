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
        "restaurant",
        "education",
        "place_of_birth",
        "citizenship",
        "personnel_number",
        "medical_checkup",
        "employment_contract",
        "work_experience",
        "image",
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

    @admin.display(empty_value='???')
    def phone_number(self, obj):
        return obj.user.phone_number

    @admin.display(empty_value='???')
    def email(self, obj):
        return obj.user.email
