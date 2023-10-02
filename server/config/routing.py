import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# from apps.chat.routing import restaurant_websocket_urlpatterns
from apps.core.middleware import JWTQueryParamAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


application = ProtocolTypeRouter({
  # 'http': get_asgi_application(),
  # 'websocket': JWTQueryParamAuthMiddleware(
  #   URLRouter(restaurant_websocket_urlpatterns),
  # ),
})
