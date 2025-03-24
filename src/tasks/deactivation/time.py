import logging
from sqlalchemy import update
from asgiref.sync import async_to_sync
from src.core.dependencies.database import get_db
from src.db.models.booking import Time
from src.db.repository import CRUDRepository
from ..celery_worker import celery_app


logger = logging.getLogger(__name__)


class DeactivateTimeTask:

    def __init__(self, crud_repository: CRUDRepository):
        self.crud_repository = crud_repository

    @celery_app.task(name="tasks.deactivation.time.deactivate_time")
    def deactivate_time(self, time_id: int):
        logger.info("Launch task to deactivate time")
        async_to_sync(self._deactivate_time)(time_id)

    async def _deactivate_time(self, time_id: int):
        async for session in get_db():
            result = await self.crud_repository.update(
                update(Time).filter(Time.id == time_id).values(is_active=False), session
            )
        if result:
            logger.info(f"Time {time_id} successfully deactivated")
        else:
            logger.warning(f"Time {time_id} not found")
