from django.urls import path

from apps.restaurants.consumers import RestaurantConsumer

chat_websocket_urlpatterns = [
    path('ws/restaurant/<restaurant_id>/', RestaurantConsumer.as_asgi()),
]
