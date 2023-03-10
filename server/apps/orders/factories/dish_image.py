from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField

from apps.orders.models import DishImage

from .dish import DishFactory


class DishImageFactory(DjangoModelFactory):
    """Factory for DishImage instance."""

    image = ImageField(
        color="green",
    )
    dish = SubFactory(
        DishFactory,
    )

    class Meta:
        model = DishImage
