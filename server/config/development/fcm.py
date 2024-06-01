import os

from firebase_admin import initialize_app

options = {
    "projectId": os.getenv("FCM_PROJECT_ID"),
}

FIREBASE_APP = initialize_app(options=options)

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "django_fcm",
    "DEFAULT_FIREBASE_APP": None,
    "FCM_SERVER_KEY": os.getenv("FCM_SERVER_KEY"),
    "ONE_DEVICE_PER_USER": True,
}
