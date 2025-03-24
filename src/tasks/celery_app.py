from celery.schedules import crontab
from core.config import settings


class CeleryConfig:
    broker_url = settings.redis_url
    result_backend = settings.redis_url
    timezone = "Europe/Kyiv"
    broker_connection_retry_on_startup = True

    include = [
        "tasks.reminders.reminder",
        "tasks.deactivation.booking",
        "tasks.deactivation.date",
        "tasks.deactivation.time",
    ]

    task_routes = {
        "tasks.reminders.reminder.*": {"queue": "reminders"},
        "tasks.deactivation.booking.*": {"queue": "deactivate"},
        "tasks.deactivation.date.*": {"queue": "deactivate"},
        "tasks.deactivation.time.*": {"queue": "deactivate"},
    }

    beat_schedule = {
        "check-subscriptions-daily": {
            "task": "tasks.reminders.reminder.check_subscriptions",
            "schedule": crontab(hour=9, minute=0),
            "options": {"queue": "reminders"},
        },
    }
