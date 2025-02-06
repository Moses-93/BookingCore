import logging
import datetime
from sqlalchemy import update
from asgiref.sync import async_to_sync
from core.dependencies import get_db
from db.models import Date
from db.crud import new_crud
from .celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.deactivate_dates.deactivate_date")
def deactivate_date(booking_id: int):
    async_to_sync(deactivate_date_async)(booking_id)


async def deactivate_date_async(
    date_id: int,
):
    logger.info("Starting task to deactivate date")
    query = update(Date).filter(Date.id == date_id).values(active=False)
    async for session in get_db():
        result = await new_crud.update(query, session)
    if result:
        logger.info(f"Date {date_id} successfully deactivated")
    else:
        logger.warning(f"Date {date_id} not found")


async def schedule_deactivate_dates(date_id: int, delete_time: datetime.datetime):
    logger.info("Starting schedule to deactivate date")
    delay = (delete_time - datetime.datetime.now()).total_seconds()
    deactivate_date.apply_async(args=[date_id], countdown=int(delay))
