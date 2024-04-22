from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from config import celery_app


@celery_app.task
def send_notification(
    filter_params: dict,
    title: str,
    body: str,
):
    FCMDevice.objects.filter(**filter_params).send_message(
        Message(
            Notification(
                title=title,
                body=body,
            ),
        ),
    )
