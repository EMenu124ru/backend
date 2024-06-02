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
    surname = Faker(
        "first_name",
    )
    email = Faker(
        "email",
    )
    password = Faker(
        "password",
    )
    phone_number = Faker(
        "phone_number",
    )
    date_of_birth = Faker(
        "date_time",
    )
    address = Faker(
        "address",
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs["phone_number"] = kwargs["phone_number"].replace("-", "").replace(" ", "")[:17]
        obj = model_class(*args, **kwargs)
        obj.save()
        return obj

    class Meta:
        django_get_or_create = (
            "username",
            "phone_number",
        )
        model = User
