from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory, ImageField
from . import models
from apps.reviews.factories import ReviewFactory


class RestaurantFactory(DjangoModelFactory):
    """Factory for Restaurant instance."""

    address = Faker(
        "address",
    )
    reviews = SubFactory(
        ReviewFactory,
    )

    class Meta:
        model = models.Restaurant


class ScheduleFactory(DjangoModelFactory):
    """Factory for Schedule instance."""

    restaurant = SubFactory(
        RestaurantFactory,
    )
    time_open = Faker(
        "time",
    )
    time_close = Faker(
        "time",
    )
    week_day = fuzzy.FuzzyChoice(
        [item for item in models.Schedule.WeekDays.choices],
    )

    class Meta:
        model = models.Schedule
