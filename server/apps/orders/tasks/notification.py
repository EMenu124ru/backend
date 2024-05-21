from django.conf import settings
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from config import celery_app


@celery_app.task
def send_notification(
    filter_params: dict,
    title: str,
    body: str,
):
    if not settings.DEBUG:
        response = FCMDevice.objects.filter(**filter_params).send_message(
            Message(
                notification=Notification(
                    title=title,
                    body=body,
                ),
            ),
        )
        print(response)
        return response.response.success_count, response.response.failure_count
