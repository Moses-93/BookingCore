import logging
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies.database import get_db
from src.core.dependencies.auth import get_current_user
from src.db.models.user import User
from src.schemas import date, time
from src.core.dependencies.auth import requires_role
from src.services.schedule.schedule_manager import ScheduleManager


logger = logging.getLogger(__name__)


class ScheduleHandler:

    def __init__(self, schedule_manager: ScheduleManager):
        self.schedule_manager = schedule_manager

    @requires_role(["master", "client"])
    async def get_dates(
        self,
        master_id: int | None = Query(None),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        logger.info("Launching the handler to get dates")
        dates = await self.schedule_manager.get_dates(db, user, master_id)
        return dates

    @requires_role(["master"])
    async def create_date(
        self,
        date: date.DateCreate,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        logger.info("Launching the handler to create date")
        created_date = await self.schedule_manager.create_date(db, user.id, date)
        return created_date

    @requires_role(["master"])
    async def deactivate_date(
        self,
        date_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        logger.info("Launching the handler to update date")
        result = await self.schedule_manager.deactivate_date(db, date_id)

    @requires_role(["master", "client"])
    async def get_times(
        self,
        master_id: int | None = Query(None),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        logger.info("Launching the handler to get times")
        times = await self.schedule_manager.get_times(db, user, master_id)
        return times

    @requires_role(["master"])
    async def create_time(
        self,
        time: time.TimeCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        logger.info("Launching the handler to create time")
        created_time = await self.schedule_manager.create_time(db, user.id, time)
        logger.info(f"Time {time.time} for date_id {time.date_id} created successfully")
        return created_time

    @requires_role(["master"])
    async def deactivate_time(
        self,
        time_id: int,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        logger.info("Launching the handler to update time")
        await self.schedule_manager.deactivate_time(db, time_id)
