from config.development import *  # noqa F403 F401 F405

SIMPLE_JWT_PROD = {
    'AUTH_COOKIE_ACCESS': 'access',
    'AUTH_COOKIE_REFRESH': 'refresh',
    'AUTH_COOKIE_DOMAIN': None,
    'AUTH_COOKIE_SECURE': False,
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'Lax',
}
SIMPLE_JWT = {**SIMPLE_JWT, **SIMPLE_JWT_PROD}  # noqa F405
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (  # noqa F405
    'apps.core.utils.authenticate.CustomAuthentication',
)
