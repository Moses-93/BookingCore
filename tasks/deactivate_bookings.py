import logging
import datetime
from sqlalchemy import update
from asgiref.sync import async_to_sync
from core.dependencies import get_db
from db.models import Booking
from db.crud import new_crud
from .celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.deactivate_bookings.deactivate_booking")
def deactivate_booking(booking_id: int):
    async_to_sync(deactivate_booking_async)(booking_id)


async def deactivate_booking_async(
    booking_id: int,
):
    logger.info("Starting task to deactivate booking")
    query = update(Booking).filter(Booking.id == booking_id).values(active=False)
    async for session in get_db():
        result = await new_crud.update(query, session)
    if result:
        logger.info(f"Booking {booking_id} successfully deactivated")
    else:
        logger.warning(f"Booking {booking_id} not found")


async def schedule_deactivate_bookings(
    booking_id: int, date: datetime.date, time: datetime.time
):
    logger.info("Starting schedule to deactivate booking")
    deactivate_time = datetime.datetime.combine(date, time)
    delay = (deactivate_time - datetime.datetime.now()).total_seconds()
    deactivate_booking.apply_async(args=[booking_id], countdown=int(delay))
