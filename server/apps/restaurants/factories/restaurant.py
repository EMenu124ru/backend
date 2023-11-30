from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from apps.restaurants.models import Restaurant


PLACE_COUNT = 10


class RestaurantFactory(DjangoModelFactory):
    """Factory for Restaurant instance."""

    address = Faker(
        "address",
    )

    @post_generation
    def places(self, create, extracted, **kwargs):
        """Create places for restaurant."""
        from .place import PlaceFactory

        if not create:
            return
        places = extracted if extracted is not None else (
            PlaceFactory(restaurant=self) for _ in range(PLACE_COUNT)
        )
        self.places.add(*places)

    class Meta:
        model = Restaurant
