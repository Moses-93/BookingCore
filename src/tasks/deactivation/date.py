import logging
from sqlalchemy import update
from asgiref.sync import async_to_sync
from src.core.dependencies.database import get_db
from src.db.models.booking import Date
from src.db.repository import CRUDRepository
from ..celery_worker import celery_app


logger = logging.getLogger(__name__)


class DeactivateDateTask:

    def __init__(self, crud_repository: CRUDRepository):
        self.crud_repository = crud_repository

    @celery_app.task(name="tasks.deactivation.date.deactivate_date")
    def deactivate_date(self, date_id: int):
        logger.info("Launch task to deactivate date")
        async_to_sync(self._deactivate_date)(date_id)

    async def _deactivate_date(self, date_id: int):
        async for session in get_db():
            result = await self.crud_repository.update(
                update(Date).filter(Date.id == date_id).values(is_active=False), session
            )
        if result:
            logger.info(f"Date {date_id} successfully deactivated")
        else:
            logger.warning(f"Date {date_id} not found")
