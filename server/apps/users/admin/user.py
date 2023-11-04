from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.forms import UserChangeFormNew, UserCreationFormNew
from apps.users.models import User


class UserAdminNew(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'surname')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    form = UserChangeFormNew
    add_form = UserCreationFormNew
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'surname')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'surname')


admin.site.register(User, UserAdminNew)
