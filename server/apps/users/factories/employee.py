from factory import (
    Faker,
    SubFactory,
    fuzzy,
    post_generation,
)
from factory.django import DjangoModelFactory

from apps.core.factories import ObjectFileFactory
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
    education = Faker(
        "company",
    )
    place_of_birth = Faker(
        "company",
    )
    citizenship = Faker(
        "company",
    )
    personnel_number = Faker(
        "pyint",
        min_value=0,
        max_value=10000,
        step=1,
    )
    medical_checkup = Faker(
        "date",
    )
    employment_contract = Faker(
        "day_of_week",
    )
    work_experience = Faker(
        "day_of_month",
    )
    image = SubFactory(
        ObjectFileFactory,
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
