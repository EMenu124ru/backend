from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.core.services.pagination import PaginationObject
from apps.restaurants.models import Restaurant
from apps.restaurants.serializers import RestaurantSerializer
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer


class RestaurantRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.prefetch_related(
            "plans",
            "schedules",
        ).filter(pk=self.kwargs["pk"])


class ReviewsRestaurantAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer
    pagination_class = PaginationObject

    def get_queryset(self):
        return Review.objects.filter(
            restaurant=self.kwargs["pk"],
        )


class RestaurantListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantSerializer
    pagination_class = PaginationObject

    def get_queryset(self):
        return Restaurant.objects.prefetch_related(
            "plans",
            "schedules",
        ).all()
