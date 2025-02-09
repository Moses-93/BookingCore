import logging
import datetime
from sqlalchemy import update
from asgiref.sync import async_to_sync
from core.dependencies import get_db
from db.models import Time
from db.crud import new_crud
from .celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.deactivate_times.deactivate_time")
def deactivate_time(booking_id: int):
    async_to_sync(deactivate_time_async)(booking_id)


async def deactivate_time_async(time_id):
    query = update(Time).filter(Time.id == time_id).values(active=False)
    async for session in get_db():
        result = await new_crud.update(query, session)
    if result:
        logger.info(f"Time {time_id} successfully deactivated")
    else:
        logger.warning(f"Time {time_id} not found")


async def schedule_deactivate_time(
    time_id: int, date: datetime.date, time: datetime.time
):
    combine_time = datetime.datetime.combine(date, time)
    delete_time = combine_time - datetime.timedelta(hours=1)
    delay = (delete_time - datetime.datetime.now()).total_seconds()
    if delay <= 0:
        logger.warning(f"Час: {time} має минуле значення.")
        return
    deactivate_time.apply_async(args=[time_id], countdown=int(delay))
    logger.info(f"Запланована деактивація часу {time} через {delay} секунд.")
