import os

from config.development import *  # noqa F403 F401 F405

SIMPLE_JWT_PROD = {
    'AUTH_COOKIE_ACCESS': 'access',
    'AUTH_COOKIE_REFRESH': 'refresh',
    'AUTH_COOKIE_DOMAIN': None,
    'AUTH_COOKIE_SECURE': False,
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'Strict',
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
CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS[::]

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
