from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField

from apps.reviews.models import ReviewImages

from .review import ReviewFactory


class ReviewImagesFactory(DjangoModelFactory):
    """Factory for ReviewImages instance."""

    image = ImageField(
        color="green",
    )
    review = SubFactory(
        ReviewFactory,
    )

    class Meta:
        model = ReviewImages
