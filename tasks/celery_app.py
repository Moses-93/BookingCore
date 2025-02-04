from celery import Celery
from core.config import settings


celery_app = Celery("tasks", broker=settings.redis_url, include=["tasks.reminders"])

celery_app.conf.update(
    timezone="UTC",
    task_routes={"tasks.reminders.send_reminder": {"queue": "reminders"}},
)

celery_app.autodiscover_tasks(["tasks"])
