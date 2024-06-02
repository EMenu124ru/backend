from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from apps.users.models import User


class UserCreationFormNew(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "phone_number",
            "last_name",
            "first_name",
            "surname",
        )
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(),
        }


class UserChangeFormNew(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(),
        }
