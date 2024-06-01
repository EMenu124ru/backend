DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.forms",
    'drf_api_logger',
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "daphne",
    "django_celery_beat",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    'rest_framework_simplejwt',
    'fcm_django',
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.restaurants.apps.RestaurantsConfig",
    "apps.users.apps.UsersConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
