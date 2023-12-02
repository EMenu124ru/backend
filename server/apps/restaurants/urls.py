from django.urls import path

from apps.restaurants.views import (
    RestaurantListAPIView,
    RestaurantPlacesAPIView,
    TagToPlaceAPIView,
)

urlpatterns = [
    path("", RestaurantListAPIView.as_view(), name="restaurants-list"),
    path("places", RestaurantPlacesAPIView.as_view(), name="restaurants-places"),
    path("tags", TagToPlaceAPIView.as_view(), name="restaurants-tags"),
]
