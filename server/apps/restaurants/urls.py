from django.urls import path

from apps.restaurants.views import RestaurantListAPIView, RestaurantRetrieveAPIView

urlpatterns = [
    path("", RestaurantListAPIView.as_view(), name="restaurants-list"),
    path("<int:pk>/", RestaurantRetrieveAPIView.as_view(), name="restaurants-detail"),
]
