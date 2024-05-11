from random import randint
from datetime import date, timedelta

from django.utils import timezone
from factory import (
    Faker,
    LazyAttribute,
    SubFactory,
    fuzzy,
)
from factory.django import DjangoModelFactory

from apps.core.models import ScheduleBase
from apps.users.models import Schedule

from .employee import EmployeeFactory


class ScheduleFactory(DjangoModelFactory):
    """Factory for Schedule instance."""

    employee = SubFactory(
        EmployeeFactory,
    )
    time_start = LazyAttribute(
        lambda _: timezone.now()
    )
    time_finish = LazyAttribute(
        lambda obj: obj.time_start + timedelta(hours=8),
    )
    is_approve = Faker(
        "pybool",
    )
    day = LazyAttribute(
        lambda _: date.today() + timedelta(days=randint(1, 10)),
    )
    type = fuzzy.FuzzyChoice(
        [item[0] for item in Schedule.Types.choices],
    )
    week_day = fuzzy.FuzzyChoice(
        [item[0] for item in ScheduleBase.WeekDays.choices],
    )

    class Meta:
        model = Schedule
        django_get_or_create = (
            "employee",
            "time_start",
        )
