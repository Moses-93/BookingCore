import logging
from httpx import RequestError
from core.config import settings
from .http_client import HTTPClient


logger = logging.getLogger(__name__)


class NotificationService:

    token = settings.telegram_main_token
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    async def send_message(self, chat_id: int, message: str):

        params = {"chat_id": chat_id, "text": message}
        async with HTTPClient() as client:
            try:
                response = await client.get(self.url, params=params)
                if response.status_code != 200:
                    logger.error(f"Помилка {response.status_code}: {response.text}")
            except RequestError as e:
                logger.error(f"Помилка при відправленні повідомлення: {e}")


notification_service = NotificationService()
