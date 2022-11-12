from factory import Faker
from factory.django import DjangoModelFactory

from apps.restaurants.models import Restaurant


class RestaurantFactory(DjangoModelFactory):
    """Factory for Restaurant instance."""

    address = Faker(
        "address",
    )

    class Meta:
        model = Restaurant
