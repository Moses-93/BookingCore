import logging
from datetime import date, time, datetime
from sqlalchemy import update
from asgiref.sync import async_to_sync
from src.core.dependencies.database import get_db
from src.db.models.booking import Booking
from src.db.repository import CRUDRepository
from ..celery_worker import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.deactivation.booking.deactivate")
def deactivate(booking_id: int):
    logger.info("Launch task to deactivate booking")
    async_to_sync(deactivate_booking_async)(booking_id)


async def deactivate_booking_async(
    booking_id: int,
):
    query = update(Booking).filter(Booking.id == booking_id).values(is_active=False)
    async for session in get_db():
        result = await new_crud.update(query, session)
    if result:
        logger.info(f"Booking {booking_id} successfully deactivated")
    else:
        logger.warning(f"Booking {booking_id} not found")


async def schedule_deactivate_booking(booking_id: int, date: date, time: time):
    logger.info("Launch scheduler to deactivate booking")
    deactivate_time = datetime.combine(date, time)
    delay = (deactivate_time - datetime.now()).total_seconds()
    deactivate.apply_async(args=[booking_id], countdown=int(delay))
