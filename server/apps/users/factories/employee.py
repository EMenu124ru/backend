from factory import (
    SubFactory,
    fuzzy,
    post_generation,
)
from factory.django import DjangoModelFactory

from apps.restaurants.factories import RestaurantFactory
from apps.users.models import Employee

from .user import UserFactory

EMPLOYEE_SCHEDULE_COUNT = 5


class EmployeeFactory(DjangoModelFactory):
    """Factory for Employee instance."""

    user = SubFactory(
        UserFactory,
    )
    role = fuzzy.FuzzyChoice(
        [item[0] for item in Employee.Roles.choices],
    )
    restaurant = SubFactory(
        RestaurantFactory,
    )

    @post_generation
    def schedule(self, create, extracted, **kwargs):
        """Create schedule for employee."""
        from .schedule import ScheduleFactory

        if not create:
            return
        schedule = extracted if extracted is not None else (
            ScheduleFactory(employee=self) for _ in range(EMPLOYEE_SCHEDULE_COUNT)
        )
        self.schedule.add(*schedule)

    class Meta:
        model = Employee
