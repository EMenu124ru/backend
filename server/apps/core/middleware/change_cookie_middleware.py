from django.conf import settings
from django.urls import reverse


class ChangeCookieMiddleware:
    URLS_IGNORE_COOKIE = {
        "post": [
            reverse("api:clients-list"),
            reverse("api:staff-login"),
            reverse("api:client-login"),
        ],
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        urls = self.URLS_IGNORE_COOKIE.get(request.method.lower())
        if urls and request.path in urls:
            request.COOKIES = {}
        else:
            token = request.COOKIES.get(settings.CSRF_COOKIE_NAME)
            if token:
                request.META[settings.CSRF_HEADER_NAME] = token
        return self.get_response(request)
