from datetime import (
    date,
    datetime,
    time,
    timedelta,
)

from factory import (
    LazyAttribute,
    SubFactory,
    fuzzy,
)
from factory.django import DjangoModelFactory

from apps.restaurants.models import Schedule

from .restaurant import RestaurantFactory


class ScheduleFactory(DjangoModelFactory):
    """Factory for Schedule instance."""

    restaurant = SubFactory(
        RestaurantFactory,
    )
    time_start = LazyAttribute(
        lambda _: datetime(2023, 1, 1, 10).strftime("%H:%M:%S")
    )
    time_finish = LazyAttribute(
        lambda obj: datetime.combine(date.today(), time.fromisoformat(obj.time_start)) + timedelta(hours=8),
    )
    week_day = fuzzy.FuzzyChoice(
        [item[0] for item in Schedule.WeekDays.choices],
    )

    class Meta:
        model = Schedule
        django_get_or_create = (
            "restaurant",
            "week_day",
        )
