import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings
from django.core.asgi import get_asgi_application

from apps.core.middleware import JWTCookieAuthMiddlewareStack, JWTQueryParamAuthMiddleware
from apps.restaurants.routing import chat_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.development')

middleware = (
  JWTQueryParamAuthMiddleware
  if settings.DEBUG else
  JWTCookieAuthMiddlewareStack
)


application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': middleware(
    URLRouter(chat_websocket_urlpatterns),
  ),
})
