import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, datetime, time, timedelta

from src.db.models import Time, User
from src.db.repository import CRUDRepository
from src.schemas.time import TimeCreate
from src.services.user import UserService
from src.tasks.deactivation import DeactivateTimeTask
from .base_service import BaseScheduleService

logger = logging.getLogger(__name__)


class TimeScheduleService(BaseScheduleService):
    def __init__(
        self,
        crud_repository: CRUDRepository,
        user_service: UserService,
        deactivation_task: DeactivateTimeTask,
    ):
        super().__init__(crud_repository, user_service, Time)
        self.deactivation_task = deactivation_task

    async def schedule_deactivate_time(self, time_id: int, date: date, time: time):
        logger.info("Launch scheduler to deactivate time")
        combine_time = datetime.combine(date, time)
        delete_time = combine_time - timedelta(hours=2)
        delay = (delete_time - datetime.now()).total_seconds()
        if delay <= 0:
            logger.warning(f"Time: {combine_time} has a past value.")
            return
        self.deactivation_task.deactivate_time.apply_async(
            args=[time_id], countdown=int(delay)
        )
        logger.info(f"Scheduled deactivation at {time} in {delay} seconds.")

    async def create_time(
        self,
        session: AsyncSession,
        user_id: int,
        time_data: TimeCreate,
    ) -> Optional[Time]:
        logger.info("Starting a business logic to create time")
        time_data_dump = time_data.model_dump(exclude="date")
        created_time = await self.create(session, user_id, time_data_dump)

        await self.schedule_deactivate_time(
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
