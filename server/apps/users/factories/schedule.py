from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from random import randint

from factory import (
    Faker,
    LazyAttribute,
    SubFactory,
)
from factory.django import DjangoModelFactory

from apps.users.models import Schedule

from .employee import EmployeeFactory


class ScheduleFactory(DjangoModelFactory):
    """Factory for Schedule instance."""

    employee = SubFactory(
        EmployeeFactory,
    )
    time_start = Faker(
        "time",
    )
    time_finish = LazyAttribute(
        lambda obj: datetime.combine(
            date.today(), time.fromisoformat(obj.time_start)
        ) + timedelta(hours=8),
    )
    day = LazyAttribute(
        lambda _: date.today() + timedelta(days=randint(1, 10)),
    )

    class Meta:
        model = Schedule
