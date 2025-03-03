from celery import Celery
from celery.schedules import crontab
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

celery_app.conf.beat_schedule = {
    "check-subscriptions-daily": {
        "task": "tasks.reminders.check_subscriptions",
        "schedule": crontab(hour=9, minute=0),
    },
}

celery_app.conf.update(
    timezone="Europe/Kyiv",
    broker_connection_retry_on_startup=True,
    task_routes={
        "tasks.reminders.reminder.send_reminder": {"queue": "reminders"},
        "tasks.deactivation.booking.deactivate_booking": {"queue": "deactivate"},
        "tasks.deactivation.date.deactivate_date": {"queue": "deactivate"},
        "tasks.deactivation.time.deactivate_time": {"queue": "deactivate"},
    },
)

celery_app.autodiscover_tasks(["tasks"])
