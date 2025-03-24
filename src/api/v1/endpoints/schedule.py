import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.dependencies import get_current_user
from core.dependencies import get_db
from db.models.user import User
from schemas import date, time
from decorators.permissions import requires_role
from utils.validators import ensure_resource_exists
from services.schedule.factory import ServiceFactory


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/schedules", tags=["dates"])

service_factory = ServiceFactory()

date_service = service_factory.create_date_service()
time_service = service_factory.create_time_service()


@router.get(
    "/dates", response_model=List[date.DateResponse], status_code=status.HTTP_200_OK
)
@requires_role(["master", "client"])
async def get_dates(
    master_id: int | None = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Launching the handler to get dates")
    dates = await date_service.get_dates(db, user, master_id)
    ensure_resource_exists(dates)
    return dates


@router.post("/dates", status_code=status.HTTP_201_CREATED)
@requires_role(["master", "master"])
async def create_date(
    date: date.DateCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Launching the handler to create date")
    created_date = await date_service.create_date(db, user.id, date)
    ensure_resource_exists(created_date)
    return created_date


@router.patch("/dates/{date_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def deactivate_date(
    date_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Launching the handler to update date")
    result = await date_service.deactivate_date(db, date_id)
    ensure_resource_exists(result)


@router.get(
    "/dates/times",
    response_model=list[time.TimeResponse],
    status_code=status.HTTP_200_OK,
)
@requires_role(["master", "client"])
async def get_times(
    master_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    logger.info("Launching the handler to get times")
    times = await time_service.get_times(db, user, master_id)
    ensure_resource_exists(times)
    return times


@router.post("/dates/times", status_code=status.HTTP_201_CREATED)
@requires_role(["master", "master"])
async def create_time(
    time: time.TimeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    logger.info("Launching the handler to create time")
    created_time = await time_service.create_time(db, user.id, time)
    logger.info(f"Time {time.time} for date_id {time.date_id} created successfully")
    return created_time


@router.patch("/dates/times/{time_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def deactivate_time(
    time_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    logger.info("Launching the handler to update time")
    await time_service.deactivate_time(db, time_id)
