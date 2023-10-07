from django.urls import path

from . import consumers

chat_websocket_urlpatterns = [
    path('ws/restaurant/<restaurant_id>/', consumers.RestaurantConsumer.as_asgi()),
]
