from __future__ import absolute_import

import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.development")
app = Celery("emenu")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_delayed_orders': {
        'task': 'apps.orders.tasks.delayed_orders.check_delayed_orders',
        'schedule': timedelta(seconds=30),
    },
    'send_updated_orders': {
        'task': 'apps.orders.tasks.update_orders.send_updated_orders',
        'schedule': timedelta(seconds=30),
    },
}
