from factory import Faker
from factory.django import DjangoModelFactory

from apps.orders.models import Category


class CategoryFactory(DjangoModelFactory):
    """Factory for Category instance."""

    name = Faker(
        "month_name",
    )

    class Meta:
        model = Category
