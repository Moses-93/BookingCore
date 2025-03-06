import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.dependencies import verify_user
from core.dependencies import get_db
from db.crud import crud
from db.models.booking import Date
from db.models.user import User
from schemas import date
from decorators.permissions import requires_role
from utils.validators import ensure_resource_exists, check_number_masters
from tasks.deactivate_dates import schedule_deactivate_dates


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dates", tags=["dates"])


@router.get("/", response_model=List[date.DateResponse], status_code=status.HTTP_200_OK)
@requires_role(["master", "client", "master"])
async def get_dates(
    master_id: int | None = Query(None),
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    if master_id is None:
        master = check_number_masters(user)
        master_id = master.id

    result = await crud.read(
        model=Date,
        session=db,
        master_id=master_id,
        active=True,
    )
    dates = result.unique().scalars().all()
    logger.info(f"Dates fetched: {dates}")
    ensure_resource_exists(dates)

    return dates


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["master", "master"])
async def create_date(
    date: date.DateCreate,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):

    result = await crud.read(model=Master, session=db, user_id=user.id)
    master = result.unique().scalar_one_or_none()
    created_date = await crud.create(
        model=Date,
        session=db,
        date=date.date,
        del_time=date.del_time,
        master_id=master.id,
    )
    ensure_resource_exists(
        created_date, status_code=400, message="Failed to create date"
    )
    await schedule_deactivate_dates(created_date.id, created_date.del_time)
    return created_date


@router.patch("/{date_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def deactivate_date(
    date_id: int,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    result = await crud.delete(model=Date, session=db, id=date_id)
    ensure_resource_exists(result)
