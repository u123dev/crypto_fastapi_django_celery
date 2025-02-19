from celery import Celery
import os

from celery.schedules import crontab
from celery import shared_task

import django
django.setup()


celery_app = Celery("app")

celery_app.config_from_object("django.conf:settings", namespace="CELERY")  # for Django


from app.util.collect import collect_all
from app.tasks import task_collect_all


celery_app.conf.update(
    task_routes={
        "app.tasks.task_collect_all": {"queue": "default"},
    }
)

# celery_app.conf.beat_schedule = {
#     "collect-all-every-minute": {
#         "task": "app.tasks.task_collect_all",
#         "schedule": crontab(minute="*"),
#     }
# }


celery_app.add_periodic_task(60.0, task_collect_all.s(), name="Collect every minute")
