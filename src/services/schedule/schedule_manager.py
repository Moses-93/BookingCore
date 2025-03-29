from typing import List, Optional
from sqlalchemy import Time
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Date, User
from src.schemas.date import DateCreate
from src.schemas.time import TimeCreate
from src.services.schedule.date_service import DateScheduleService
from src.services.schedule.time_service import TimeScheduleService


class ScheduleManager:
    def __init__(
        self, date_service: DateScheduleService, time_service: TimeScheduleService
    ):
        self.date_service = date_service
        self.time_service = time_service

    async def create_date(
        self, session: AsyncSession, user_id: int, date_data: DateCreate
    ) -> Date:
        created_date = await self.date_service.create_date(session, user_id, date_data)
        await self.date_service.schedule_deactivate_date(
            created_date.id, created_date.deactivation_time
        )
        return created_date

    async def create_time(
        self,
        session: AsyncSession,
        user_id: int,
        time_data: TimeCreate,
    ) -> Time:
        created_time = await self.create_time(session, user_id, time_data)
        await self.time_service.schedule_deactivate_time(
            created_time.id, time_data.date, created_time.time
        )
        return created_time

    async def get_dates(
        self, session: AsyncSession, user: User, master_id: int
    ) -> List[Date]:
        return await self.date_service.get_dates(session, user, master_id)

    async def get_times(
        self, session: AsyncSession, user: User, master_id: int
    ) -> List[Time]:
        return await self.time_service.get_times(session, user, master_id)

    async def get_date(self, session: AsyncSession, date_id: int) -> Date:
        return await self.date_service.get_date(session, date_id)

    async def get_time(self, session: AsyncSession, time_id: int) -> Optional[Time]:
        return await self.time_service.get_time(session, time_id)

    async def deactivate_time(self, session: AsyncSession, time_id: int) -> bool:
        return await self.time_service.deactivate_time(session, time_id)

    async def deactivate_date(self, session: AsyncSession, date_id: int) -> bool:
        return await self.date_service.deactivate_date(session, date_id)
