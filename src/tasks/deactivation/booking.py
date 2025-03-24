import logging
from sqlalchemy import update
from asgiref.sync import async_to_sync
from src.core.dependencies.database import get_db
from src.db.models.booking import Booking
from src.db.repository import CRUDRepository
from ..celery_worker import celery_app


logger = logging.getLogger(__name__)


class DeactivateBookingTask:
    def __init__(self, crud_repository: CRUDRepository):
        self.crud_repository = crud_repository

    @celery_app.task(name="tasks.deactivation.booking.deactivate_booking")
    def deactivate_booking(self, booking_id: int):
        logger.info("Launch task to deactivate booking")
        async_to_sync(self._deactivate_booking)(booking_id)

    async def _deactivate_booking(
        self,
        booking_id: int,
    ):
        async for session in get_db():
            result = await self.crud_repository.update(
                update(Booking)
                .filter(Booking.id == booking_id)
                .values(is_active=False),
                session,
            )
        if result:
            logger.info(f"Booking {booking_id} successfully deactivated")
        else:
            logger.warning(f"Booking {booking_id} not found")
