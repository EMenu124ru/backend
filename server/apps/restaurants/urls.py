from django.urls import path

from apps.restaurants.views import (
    RestaurantListAPIView,
    RestaurantPlacesAPIView,
    TagToPlaceAPIView,
)

urlpatterns = [
    path("", RestaurantListAPIView.as_view(), name="restaurants-list"),
    path("<int:pk>/places", RestaurantPlacesAPIView.as_view(), name="restaurants-places"),
    path("<int:pk>/tags", TagToPlaceAPIView.as_view(), name="restaurants-tags"),
]
