import logging
from datetime import datetime
from sqlalchemy import update
from asgiref.sync import async_to_sync
from core.dependencies import get_db
from db.models.booking import Date
from db.crud import new_crud
from ..celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.deactivation.date.deactivate")
def deactivate(booking_id: int):
    logger.info("Launch task to deactivate date")
    async_to_sync(deactivate_date_async)(booking_id)


async def deactivate_date_async(
    date_id: int,
):
    query = update(Date).filter(Date.id == date_id).values(is_active=False)
    async for session in get_db():
        result = await new_crud.update(query, session)
    if result:
        logger.info(f"Date {date_id} successfully deactivated")
    else:
        logger.warning(f"Date {date_id} not found")


async def schedule_deactivate_date(date_id: int, deactivate_time: datetime):
    logger.info("Launch scheduler to deactivate date")
    delay = (deactivate_time - datetime.now()).total_seconds()
    if delay <= 0:
        logger.warning(f"date has a past value.")
        return
    deactivate.apply_async(args=[date_id], countdown=int(delay))
