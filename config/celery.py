import os

from django.conf import settings

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("proj")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()
CELERY_IMPORTS = ("tasks",)


app.conf.beat_schedule = {
    "add-every-60-seconds": {
        "task": "bots.tasks.send_notification",
        "schedule": 60.0,
    },
}
app.conf.timezone = "UTC"
