from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from apps.restaurants.models import Restaurant

PLACE_COUNT = 10
SCHEDULES_COUNT = 7


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

    @post_generation
    def schedule(self, create, extracted, **kwargs):
        """Create schedule for restaurant."""
        from .schedule import ScheduleFactory

        if not create:
            return
        schedule = extracted if extracted is not None else (
            ScheduleFactory(restaurant=self) for _ in range(SCHEDULES_COUNT)
        )
        self.schedule.add(*schedule)

    class Meta:
        model = Restaurant
