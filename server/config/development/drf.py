from datetime import timedelta

# django-rest-framework
# -------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "EXCEPTION_HANDLER": "apps.core.utils.custom_exception_handler",
}

CORS_ALLOWED_ORIGINS = []

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('JWT',),
}
