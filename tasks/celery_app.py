from celery import Celery
from core.config import settings


celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    include=[
        "tasks.reminders",
        "tasks.deactivate_bookings",
        "tasks.deactivate_dates",
        "tasks.deactivate_times",
    ],
)

celery_app.conf.update(
    timezone="UTC",
    task_routes={
        "tasks.reminders.send_reminder": {"queue": "reminders"},
        "tasks.deactivate_bookings.deactivate_booking": {
            "queue": "deactivate_bookings"
        },
        "tasks.deactivate_dates.deactivate_date": {"queue": "deactivate_dates"},
        "tasks.deactivate_times.deactivate_time": {"queue": "deactivate_times"},
    },
)

celery_app.autodiscover_tasks(["tasks"])
