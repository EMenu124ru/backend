from django.urls import path

from apps.restaurants.views import RestaurantListAPIView, ReviewsRestaurantAPIView

urlpatterns = [
    path("", RestaurantListAPIView.as_view(), name="restaurants-list"),
    path("<int:pk>/reviews", ReviewsRestaurantAPIView.as_view(), name="restaurants-reviews"),
]
