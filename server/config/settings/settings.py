import os
from pathlib import Path

import dj_database_url

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    default="qaEhm3Sc0WuO93idsME1e7vmiwWpuLqTJX6PRRyBpgUUDPQPqhBObwZ6UgqT6OuG",
)
TIME_ZONE = "Asia/Krasnoyarsk"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

if allowed_hosts := os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = [
        origin.strip() for origin in allowed_hosts.split(',')
    ]
else:
    ALLOWED_HOSTS = ["*"]

# DATABASES
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DATABASES = {'default': dj_database_url.config(conn_max_age=60)}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
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
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
ADMIN_URL = os.getenv(
    "DJANGO_ADMIN_URL",
    "admin/",
)

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
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
if DEBUG:
    from .installed_apps import INSTALLED_APPS
    import socket

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
