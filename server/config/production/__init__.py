import os

from config.development import *  # noqa F403 F401 F405

CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_PATH = "/"
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = os.getenv("SERVER_HOST")
CSRF_COOKIE_AGE = 60 * 60 * 24 * 30 * 12
CSRF_COOKIE_NAME = "csrftoken"

CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'

MIDDLEWARE = (
    ["apps.core.middleware.change_cookie_middleware.ChangeCookieMiddleware"] +
    MIDDLEWARE  # noqa F405
)

SIMPLE_JWT_PROD = {
    'AUTH_COOKIE_ACCESS': 'access',
    'AUTH_COOKIE_REFRESH': 'refresh',
    'AUTH_COOKIE_SECURE': CSRF_COOKIE_SECURE,
    'AUTH_COOKIE_HTTP_ONLY': CSRF_COOKIE_HTTPONLY,
    'AUTH_COOKIE_PATH': CSRF_COOKIE_PATH,
    'AUTH_COOKIE_SAMESITE': CSRF_COOKIE_SAMESITE,
    'AUTH_COOKIE_EXPIRES': CSRF_COOKIE_AGE,
}
SIMPLE_JWT = {**SIMPLE_JWT, **SIMPLE_JWT_PROD}  # noqa F405
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (  # noqa F405
    'apps.core.utils.authenticate.CustomAuthentication',
)

if allowed_hosts := os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = [
        origin.strip() for origin in allowed_hosts.split(',')
    ]

if cors_origins := os.getenv('CORS_ALLOWED_ORIGINS'):
    CORS_ALLOWED_ORIGINS = [
        origin.strip() for origin in cors_origins.split(',')
    ]
CORS_ORIGIN_WHITELIST = CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS[::]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = ["*"]
