from django.urls import reverse


class IgnoreCookieMiddleware:
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
        print(request.COOKIES)
        if urls and request.path in urls:
            request.COOKIES = {}
        print(request.COOKIES)
        response = self.get_response(request)
        print(request.COOKIES)
        return response
