import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.dependencies import get_current_user
from core.dependencies import get_db
from db.models.user import User
from schemas import date
from decorators.permissions import requires_role
from utils.validators import ensure_resource_exists
from services.datetime_service import date_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dates", tags=["dates"])


@router.get("/", response_model=List[date.DateResponse], status_code=status.HTTP_200_OK)
@requires_role(["master", "client"])
async def get_dates(
    master_id: int | None = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    dates = await date_service.get_dates(db, user, master_id)
    ensure_resource_exists(dates)
    return dates


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["master", "master"])
async def create_date(
    date: date.DateCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    created_date = await date_service.create_date(db, user.id, date)
    ensure_resource_exists()
    return created_date


@router.patch("/{date_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def deactivate_date(
    date_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await date_service.deactivate_date(db, date_id)
    ensure_resource_exists(result)
