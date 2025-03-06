import logging

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from core.dependencies import get_db
from db.models.user import User
from schemas.time import TimeCreate, TimeResponse
from decorators.permissions import requires_role
from utils.validators import ensure_resource_exists
from services.datetime_service import time_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/times", tags=["times"])


@router.get("/", response_model=list[TimeResponse], status_code=status.HTTP_200_OK)
@requires_role(["master", "client"])
async def get_times(
    master_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    times = await time_service.get_times(db, user, master_id)
    ensure_resource_exists(times)
    return times


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["master", "master"])
async def create_time(
    time: TimeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    created_time = await time_service.create_time(db, time)
    logger.info(f"Time {time.time} for date_id {time.date_id} created successfully")
    return created_time


@router.patch("/{time_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def deactivate_time(
    time_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await time_service.deactivate_time(db, time_id)
