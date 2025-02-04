import logging
import requests
from core.config import settings


logger = logging.getLogger(__name__)

TOKEN = settings.telegram_sender_token
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message(chat_id: int, message: str):

    params = {"chat_id": chat_id, "text": message}

    try:
        response = requests.get(URL, params=params, timeout=5)
        if response.status_code != 200:
            logger.error(f"Помилка {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Помилка при відправленні повідомлення: {e}")
