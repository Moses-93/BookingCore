import logging
from datetime import date, time, timedelta, datetime
from sqlalchemy import update
from asgiref.sync import async_to_sync
from core.dependencies import get_db
from db.models.booking import Time
from db.crud import new_crud
from ..celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.deactivation.time.deactivate")
def deactivate(time_id: int):
    logger.info("Launch task to deactivate time")
    async_to_sync(deactivate_time_async)(time_id)


async def deactivate_time_async(time_id):
    query = update(Time).filter(Time.id == time_id).values(is_active=False)
    async for session in get_db():
        result = await new_crud.update(query, session)
    if result:
        logger.info(f"Time {time_id} successfully deactivated")
    else:
        logger.warning(f"Time {time_id} not found")


async def schedule_deactivate_time(time_id: int, date: date, time: time):
    logger.info("Launch scheduler to deactivate time")
    combine_time = datetime.combine(date, time)
    delete_time = combine_time - timedelta(hours=2)
    delay = (delete_time - datetime.now()).total_seconds()
    if delay <= 0:
        logger.warning(f"Time: {combine_time} has a past value.")
        return
    deactivate.apply_async(args=[time_id], countdown=int(delay))
    logger.info(f"Scheduled deactivation at {time} in {delay} seconds.")
