import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from db.models import Date, User
from db.repository import CRUDRepository
from schemas.date import DateCreate
from services.user import UserService
from tasks.deactivation import DeactivateDateTask
from .base_service import BaseScheduleService

logger = logging.getLogger(__name__)


class DateScheduleService(BaseScheduleService):
    def __init__(
        self,
        crud_repository: CRUDRepository,
        user_service: UserService,
        deactivation_task: DeactivateDateTask,
    ):
        super().__init__(crud_repository, user_service, Date)
        self.deactivation_task = deactivation_task

    async def schedule_deactivate_date(self, date_id: int, deactivate_time: datetime):
        logger.info("Launch scheduler to deactivate date")
        delay = (deactivate_time - datetime.now()).total_seconds()
        if delay <= 0:
            logger.warning(f"date has a past value.")
            return
        self.deactivation_task.deactivate_date.apply_async(
            args=[date_id], countdown=int(delay)
        )

    async def create_date(
        self, session: AsyncSession, user_id: int, date_data: DateCreate
    ) -> Optional[Date]:
        date_data_dump = date_data.model_dump()
        created_date = await self.create(session, user_id, date_data_dump)
        await self.schedule_deactivate_date(
            created_date.id, created_date.deactivation_time
        )
        return created_date

    async def get_dates(
        self, session: AsyncSession, user: User, master_id: int
    ) -> Optional[List[Date]]:
        return await self.get_all(session, user, master_id)

    async def get_date(self, session: AsyncSession, date_id: int) -> Optional[Date]:
        return await self.get_one(session, date_id)

    async def deactivate_date(self, session: AsyncSession, date_id: int) -> bool:
        return await self.deactivate(session, date_id)
