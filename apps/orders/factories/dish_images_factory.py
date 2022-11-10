from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField

from apps.orders.models import DishImages

from .dish_factory import DishFactory

IMAGES_COUNT = 3

class DishImagesFactory(DjangoModelFactory):
    """Factory for DishImages instance."""

    image = ImageField(
        color="green",
    )
    dish = SubFactory(
        DishFactory,
    )

    # @post_generation
    # def image(self, create, extracted, **kwargs):
    #     """Create images for review."""
    #     if not create:
    #         return
    #     images = extracted if extracted is not None else (
    #         DishImagesFactory(review=self) for _ in range(IMAGES_COUNT)
    #     )
    #     self.images.add(*images)

    class Meta:
        model = DishImages
