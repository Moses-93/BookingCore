import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional
from datetime import datetime

from db.crud import new_crud
from db.models.booking import Date, Time
from db.models.user import User
from schemas.date import DateCreate
from schemas.time import TimeCreate
from services.user import UserTools, user_tools
from tasks.task_manager import TaskManager


logger = logging.getLogger(__name__)


class DateService:

    def __init__(
        self, user_tools: UserTools, deactivation_task: TaskManager.Deactivation
    ):
        self.user_tools = user_tools
        self.deactivation_task = deactivation_task

    async def deactivation_date_scheduler(
        self, session: AsyncSession, date_id: int, deactivation_time: datetime
    ):
        await self.deactivation_task.date(session, date_id, deactivation_time)

    async def create_date(
        self, session: AsyncSession, user_id: int, date_data: DateCreate
    ) -> Optional[Date]:
        date_dump = date_data.model_dump()
        date_dump["master_id"] = user_id
        stmt = Date(**date_dump)
        created_date = await new_crud.create(stmt, session)
        await self.deactivation_date_scheduler(
            session, created_date.id, created_date.deactivation_time
        )
        return created_date

    async def get_dates(
        self, session: AsyncSession, user: User, master_id: int
    ) -> Optional[List[Date]]:
        filters = {}
        if not master_id:
            filters = await self.user_tools.identify_role(user, filters)
        result = await new_crud.read(
            select(Date).filter_by(is_active=True, **filters), session
        )
        dates = result.scalars().all()
        return dates

    async def deactivate_date(self, session: AsyncSession, date_id: int) -> bool:
        return await new_crud.update(
            update(Date).where(Date.id == date_id).values(is_active=False), session
        )


class TimeService:

    def __init__(
        self, user_tools: UserTools, deactivation_task: TaskManager.Deactivation
    ):
        self.user_tools = user_tools
        self.deactivation_task = deactivation_task

    async def deactivation_time_scheduler(
        self, session: AsyncSession, time_id: int, date: datetime, time
    ):
        await self.deactivation_task.time(session, time_id, date, time)

    async def create_time(
        self,
        session: AsyncSession,
        time_data: TimeCreate,
    ) -> Optional[Time]:
        time_data_dump = time_data.model_dump()
        stmt = Time(**time_data_dump)
        created_time = await new_crud.create(stmt, session)
        await self.deactivation_time_scheduler(
            session, created_time.id, time_data.date, created_time.time
        )
        return created_time

    async def get_times(
        self, session: AsyncSession, user: User, master_id: int
    ) -> Optional[List[Time]]:
        filters = {}
        if not master_id:
            filters = await self.user_tools.identify_role(user, filters)
        result = await new_crud.read(
            select(Time).filter_by(is_active=True, **filters), session
        )
        times = result.scalars().all()
        return times

    async def deactivate_time(self, session: AsyncSession, time_id: int) -> bool:
        return await new_crud.update(
            update(Time).where(Time.id == time_id).values(is_active=False), session
        )


date_service = DateService(user_tools, TaskManager.Deactivation)
time_service = TimeService(user_tools, TaskManager.Deactivation)
