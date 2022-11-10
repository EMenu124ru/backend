from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from apps.restaurants.models import Schedule

from .restaurant_factory import RestaurantFactory


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
        [item[0] for item in Schedule.WeekDays.choices],
    )

    class Meta:
        model = Schedule
