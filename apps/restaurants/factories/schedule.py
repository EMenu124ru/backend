from datetime import datetime, timedelta, date
from factory import Faker, SubFactory, fuzzy, LazyAttribute
from factory.django import DjangoModelFactory

from apps.restaurants.models import Schedule

from .restaurant import RestaurantFactory


class ScheduleFactory(DjangoModelFactory):
    """Factory for Schedule instance."""

    restaurant = SubFactory(
        RestaurantFactory,
    )
    time_open = Faker(
        "time",
    )
    time_close = LazyAttribute(
        lambda obj: datetime.combine(date.today(), obj.time_open) + timedelta(hours=8),
    )
    week_day = fuzzy.FuzzyChoice(
        [item[0] for item in Schedule.WeekDays.choices],
    )

    class Meta:
        model = Schedule
