from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.users.models import User


class UserCreationFormNew(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class UserChangeFormNew(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
