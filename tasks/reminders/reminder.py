from datetime import datetime
import logging

from ..celery_app import celery_app
from services.notifications import send_message


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.reminders.reminder.send_reminder")
def send_reminder(chat_id: int, message: str):
    """Sends reminder to the user"""
    logger.info("Launch task to send a reminder")
    send_message(chat_id, message)


async def schedule_reminder(chat_id: int, reminder_time: datetime, message: str):
    logger.info("Launch scheduler to send reminder")
    delay = (reminder_time - datetime.now()).total_seconds()

    if delay <= 0:
        logger.warning(
            f"Нагадування для {chat_id} має минуле значення {reminder_time}."
        )
        return

    send_reminder.apply_async(args=[chat_id, message], countdown=int(delay))
    logger.info(f"Reminder is scheduled for {chat_id} in {delay} seconds.")
