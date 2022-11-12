from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from apps.users.models import Client

from .user import UserFactory


class ClientFactory(DjangoModelFactory):
    """Factory for Client instance."""

    user = SubFactory(
        UserFactory,
    )
    bonuses = Faker(
        "pyint",
        min_value=0,
        max_value=250,
        step=1,
    )
    phone_number = Faker(
        "phone_number",
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.phone_number = obj.phone_number[:17]
        obj.save()
        return obj

    class Meta:
        django_get_or_create = (
            "phone_number",
        )
        model = Client
