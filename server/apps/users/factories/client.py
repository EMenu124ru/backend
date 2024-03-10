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

    class Meta:
        model = Client
