from rest_framework.generics import ListAPIView

from apps.core.services.pagination import PaginationObject
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers import RestaurantSerializer
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer


class ReviewsRestaurantAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = PaginationObject

    def get_queryset(self):
        return Review.objects.filter(
            restaurant=self.kwargs["pk"],
        )


class RestaurantListAPIView(ListAPIView):
    serializer_class = RestaurantSerializer
    pagination_class = PaginationObject

    def get_queryset(self):
        return Restaurant.objects.prefetch_related(
            "places",
            "schedule",
        ).all()
