from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField

from apps.reviews.models import ReviewImage

from .review import ReviewFactory


class ReviewImageFactory(DjangoModelFactory):
    """Factory for ReviewImage instance."""

    image = ImageField(
        color="green",
    )
    review = SubFactory(
        ReviewFactory,
    )

    class Meta:
        model = ReviewImage
