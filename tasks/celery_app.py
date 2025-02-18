from celery import Celery
from core.config import settings


celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    include=[
        "tasks.reminders.reminder",
        "tasks.deactivation.booking",
        "tasks.deactivation.date",
        "tasks.deactivation.time",
    ],
)

celery_app.conf.update(
    timezone="UTC",
    task_routes={
        "tasks.reminders.reminder.send_reminder": {"queue": "reminders"},
        "tasks.deactivation.booking.deactivate_booking": {"queue": "deactivate"},
        "tasks.deactivation.date.deactivate_date": {"queue": "deactivate"},
        "tasks.deactivation.time.deactivate_time": {"queue": "deactivate"},
    },
)

celery_app.autodiscover_tasks(["tasks"])
