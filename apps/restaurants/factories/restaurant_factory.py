from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from apps.restaurants.models import Restaurant


class RestaurantFactory(DjangoModelFactory):
    """Factory for Restaurant instance."""

    address = Faker(
        "address",
    )

    @post_generation
    def reviews(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for review in extracted:
                self.reviews.add(review)

    class Meta:
        model = Restaurant
