DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "daphne",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    'rest_framework_simplejwt',
]

LOCAL_APPS = [
    "apps.orders.apps.OrdersConfig",
    "apps.restaurants.apps.RestaurantsConfig",
    "apps.reviews.apps.ReviewsConfig",
    "apps.users.apps.UsersConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
