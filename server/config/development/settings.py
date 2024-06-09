import os
from datetime import datetime
from math import ceil
from pathlib import Path

import dj_database_url
from drf_api_logger import API_LOGGER_SIGNAL
from pytz import timezone

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = os.environ.get("DJANGO_DEBUG", "false") == "true"

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "qaEhm3Sc0WuO93idsME1e7vmiwWpuLqTJX6PRRyBpgUUDPQPqhBObwZ6UgqT6OuG",
)
USE_TZ = True
TIME_ZONE = "Asia/Krasnoyarsk"
LANGUAGE_CODE = "ru"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.routing.application"

PHONENUMBER_DEFAULT_REGION = "RU"

ALLOWED_HOSTS = ["*"]

# DATABASES
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DATABASES = {'default': dj_database_url.config(conn_max_age=60)}

REDIS_URL = os.getenv('REDIS_URL')

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# PASSWORDS
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(ROOT_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(ROOT_DIR / "media")
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(ROOT_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = os.getenv("DJANGO_ADMIN_URL", "admin/")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
if DEBUG:
    import socket

    from .installed_apps import INSTALLED_APPS

    def show_toolbar(request):
        from django.conf import settings
        return settings.DEBUG

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TEMPLATE_CONTEXT": show_toolbar,
    }
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INSTALLED_APPS += ['debug_toolbar']
    INTERNAL_IPS = (
        "0.0.0.0",
        "127.0.0.1",
    )
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += (ip[:-1] + "1",)

# drf-api-logger
# ------------------------------------------------------------------------------
DRF_API_LOGGER_EXCLUDE_KEYS = ["COOKIE"]
DRF_LOGGER_INTERVAL = 1
DRF_API_LOGGER_DATABASE = True
DRF_API_LOGGER_SIGNAL = True

if USE_TZ:
    utc = timezone("UTC")
    current = timezone(TIME_ZONE)
    now = datetime.now()
    DRF_API_LOGGER_TIMEDELTA = ceil((utc.localize(now) - current.localize(now).astimezone(utc)).seconds / 60)


def listener(**kwargs):
    print(kwargs)


API_LOGGER_SIGNAL.listen += listener
