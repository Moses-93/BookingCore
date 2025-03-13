import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from db.models.booking import Time
from db.models.user import User
from schemas.time import TimeCreate
from services.user import UserTools
from tasks.task_manager import TaskManager
from .base_service import BaseScheduleService

logger = logging.getLogger(__name__)


class TimeScheduleService(BaseScheduleService):
    def __init__(
        self, user_tools: UserTools, deactivation_task: TaskManager.Deactivation
    ):
        super().__init__(user_tools, Time)
        self.deactivation_task = deactivation_task

    async def deactivation_time_scheduler(self, time_id: int, date: datetime, time):
        await self.deactivation_task.time(time_id, date, time)

    async def create_time(
        self,
        session: AsyncSession,
        user_id: int,
        time_data: TimeCreate,
    ) -> Optional[Time]:
        logger.info("Starting a business logic to create time")
        time_data_dump = time_data.model_dump(exclude="date")
        created_time = await self.create(session, user_id, time_data_dump)

        await self.deactivation_time_scheduler(
            created_time.id, time_data.date, created_time.time
        )
        return created_time

    async def get_times(
        self, session: AsyncSession, user: User, master_id: int
    ) -> Optional[List[Time]]:
        return await self.get_all(session, user, master_id)

    async def get_time(self, session: AsyncSession, time_id: int) -> Optional[Time]:
        return await self.get_one(session, time_id)

    async def deactivate_time(self, session: AsyncSession, time_id: int) -> bool:
        return await self.deactivate(session, time_id)
