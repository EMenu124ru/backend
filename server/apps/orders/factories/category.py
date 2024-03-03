from factory import Faker, LazyAttribute
from factory.django import DjangoModelFactory, ImageField

from apps.core.factories import ObjectFileFactory
from apps.orders.models import Category


class CategoryFactory(DjangoModelFactory):
    """Factory for Category instance."""

    name = Faker(
        "month_name",
    )
    icon = LazyAttribute(
        lambda _: ObjectFileFactory.create(file=ImageField()),
    )

    class Meta:
        django_get_or_create = (
            "name",
        )
        model = Category
