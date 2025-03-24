import logging
from datetime import datetime
from sqlalchemy import update
from asgiref.sync import async_to_sync
from src.core.dependencies.database import get_db
from src.db.models.booking import Date
from src.db.repository import CRUDRepository
from ..celery_worker import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.deactivation.date.deactivate")
def deactivate_date(date_id: int):
    logger.info("Launch task to deactivate date")
    async_to_sync(_deactivate_date)(date_id)


async def _deactivate_date(date_id: int):
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
    deactivate_date.apply_async(args=[date_id], countdown=int(delay))
