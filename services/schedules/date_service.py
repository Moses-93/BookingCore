import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from db.models.booking import Date
from db.models.user import User
from schemas.date import DateCreate
from services.user import UserTools
from tasks.task_manager import TaskManager
from .base_service import BaseScheduleService

logger = logging.getLogger(__name__)


class DateScheduleService(BaseScheduleService):
    def __init__(
        self, user_tools: UserTools, deactivation_task: TaskManager.Deactivation
    ):
        super().__init__(user_tools, Date)
        self.deactivation_task = deactivation_task

    async def deactivation_date_scheduler(
        self, date_id: int, deactivation_time: datetime
    ):
        await self.deactivation_task.date(date_id, deactivation_time)

    async def create_date(
        self, session: AsyncSession, user_id: int, date_data: DateCreate
    ) -> Optional[Date]:
        date_data_dump = date_data.model_dump()
        created_date = await self.create(session, user_id, date_data_dump)
        await self.deactivation_date_scheduler(created_date.id, created_date.deactivation_time)
        return created_date

    async def get_dates(
        self, session: AsyncSession, user: User, master_id: int
    ) -> Optional[List[Date]]:
        return await self.get_all(session, user, master_id)
    
    async def get_date(self, session: AsyncSession, date_id: int) -> Optional[Date]:
        return await self.get_one(session, date_id)

    async def deactivate_date(self, session: AsyncSession, date_id: int) -> bool:
        return await self.deactivate(session, date_id)
