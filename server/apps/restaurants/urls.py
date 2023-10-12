from django.urls import path, re_path

from apps.restaurants.views import (
    RestaurantListAPIView,
    RestaurantRetrieveAPIView,
    ReviewsRestaurantAPIView,
)

urlpatterns = [
    path("", RestaurantListAPIView.as_view(), name="restaurants-list"),
    re_path(r"(?P<pk>[0-9]+)/$", RestaurantRetrieveAPIView.as_view(), name="restaurants-detail"),
    re_path(r"(?P<pk>[0-9]+)/reviews/$", ReviewsRestaurantAPIView.as_view(), name="restaurants-reviews"),
]
