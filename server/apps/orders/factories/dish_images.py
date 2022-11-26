from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField

from apps.orders.models import DishImages

from .dish import DishFactory


class DishImagesFactory(DjangoModelFactory):
    """Factory for DishImages instance."""

    image = ImageField(
        color="green",
    )
    dish = SubFactory(
        DishFactory,
    )

    class Meta:
        model = DishImages
