import os

from firebase_admin import initialize_app

FIREBASE_APP = initialize_app()

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "django_fcm",
    "DEFAULT_FIREBASE_APP": None,
    "FCM_SERVER_KEY": os.getenv("FCM_SERVER_KEY"),
    "ONE_DEVICE_PER_USER": False,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}
