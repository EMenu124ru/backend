from django.contrib import admin

from apps.core.models import ObjectFile


@admin.register(ObjectFile)
class ObjectFileAdmin(admin.ModelAdmin):
    """Class representation of ObjectFile model in admin panel."""

    list_display = (
        "id",
        "file",
        "filename",
    )
