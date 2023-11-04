from django.contrib import admin

from apps.users.models import Client


@admin.register(Client)
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

    @admin.display(empty_value='???')
    def surname(self, obj):
        return obj.user.surname
