from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField

from apps.reviews.models import ReviewImages

from .review_factory import ReviewFactory

IMAGES_COUNT = 3

class ReviewImagesFactory(DjangoModelFactory):
    """Factory for ReviewImages instance."""

    image = ImageField(
        color="green",
    )
    review = SubFactory(
        ReviewFactory,
    )

    # @post_generation
    # def image(self, create, extracted, **kwargs):
    #     """Create images for review."""
    #     if not create:
    #         return
    #     images = extracted if extracted is not None else (
    #         ReviewImagesFactory(review=self) for _ in range(IMAGES_COUNT)
    #     )
    #     self.images.add(*images)

    class Meta:
        model = ReviewImages
