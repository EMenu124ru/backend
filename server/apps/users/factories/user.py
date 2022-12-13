from factory import Faker
from factory.django import DjangoModelFactory

from apps.users.models import User


class UserFactory(DjangoModelFactory):
    """Factory for User instance."""

    username = Faker(
        "user_name",
    )
    first_name = Faker(
        "first_name",
    )
    last_name = Faker(
        "last_name",
    )
    email = Faker(
        "email",
    )
    password = Faker(
        "password",
    )

    class Meta:
        django_get_or_create = (
            "username",
        )
        model = User
