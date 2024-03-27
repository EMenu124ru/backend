from django.contrib.auth.forms import UserChangeForm, UserCreationForm

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


class UserChangeFormNew(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
