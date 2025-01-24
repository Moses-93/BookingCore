import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import verify_user
from core.dependencies import get_db
from db.crud import crud
from db.models import Date, User
from schemas import date
from decorators.permissions import requires_role
from utils.validators import ensure_resource_exists


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dates", tags=["dates"])


@router.get("/", response_model=list[date.DateResponse])
@requires_role(["admin", "user"])
async def get_dates(
    user: User = Depends(verify_user), db: AsyncSession = Depends(get_db)
):
    dates = await crud.read(
        model=Date,
        session=db,
    )
    ensure_resource_exists(dates)
    return dates


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["admin"])
async def create_date(
    date: date.DateCreate,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):

    created_date = await crud.create(
        model=Date, session=db, date=date.date, del_time=date.del_time
    )
    ensure_resource_exists(
        created_date, status_code=400, message="Failed to create date"
    )
    return created_date


@router.delete("/{date_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["admin"])
async def delete_date(
    date_id: int,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    result = await crud.delete(model=Date, session=db, id=date_id)
    ensure_resource_exists(result)
