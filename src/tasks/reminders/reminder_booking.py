import logging
from asgiref.sync import async_to_sync

from tasks.celery_worker import celery_app
from services.notifications import NotificationService

logger = logging.getLogger(__name__)


class BookingReminderTask:

    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    @celery_app.task(name="tasks.reminders.reminder.send_reminder")
    def send_booking_reminder(self, chat_id: int, message: str):
        """Sends reminder to the user"""
        logger.info("Launch task to send a reminder")
        async_to_sync(self._send_booking_reminder)(chat_id, message)

    async def _send_booking_reminder(self, chat_id: int, message: str):
        await self.notification_service.send_message(chat_id, message)
