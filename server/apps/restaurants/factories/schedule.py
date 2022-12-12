from datetime import date, datetime, time, timedelta

from factory import Faker, LazyAttribute, SubFactory, fuzzy
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
        lambda obj: datetime.combine(date.today(), time.fromisoformat(obj.time_open)) + timedelta(hours=8),
    )
    week_day = fuzzy.FuzzyChoice(
        [item[0] for item in Schedule.WeekDays.choices],
    )

    class Meta:
        model = Schedule
