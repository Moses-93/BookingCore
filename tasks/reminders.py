import datetime
import logging

from .celery_app import celery_app
from services.notifications import send_message


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.reminders.send_reminder")
def send_reminder(chat_id: int, message: str):
    """Відправляє нагадування користувачу"""
    logger.info("Запуск таски для надсилання нагадування")
    send_message(chat_id, message)


def schedule_reminder(
    chat_id: int,
    service: str,
    date: datetime.datetime.date,
    time: datetime.datetime.time,
    reminder_time: datetime.datetime,
):
    """Планує нагадування в Celery"""
    logger.info("Виклик функція для запуску таски нагдування")
    delay = (reminder_time - datetime.datetime.now()).total_seconds()

    if delay <= 0:
        logger.warning(
            f"Нагадування для {chat_id} має минуле значення {reminder_time}, не відправляємо задачу."
        )
        return
    message = f"Нагадуємо, у вас заплановано запис на послугу {service}. Чекаю вас {date} о {time}"

    send_reminder.apply_async(args=[chat_id, message], countdown=int(delay))
    logger.info(f"Заплановано нагадування для {chat_id} через {delay} секунд.")
