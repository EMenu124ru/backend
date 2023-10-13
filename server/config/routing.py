import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.core.middleware import JWTQueryParamAuthMiddleware
from apps.restaurants.routing import chat_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': JWTQueryParamAuthMiddleware(
    URLRouter(chat_websocket_urlpatterns),
  ),
})