import logging
from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import verify_user
from core.dependencies import get_db
from db.crud import crud
from db.models import Date, User
from schemas import date
from decorators.permissions import requires_role

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
    logger.debug(f"dates: {dates}")
    if not dates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dates not found"
        )
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
    if created_date is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create date"
        )
    return created_date


@router.delete("/{date_id}", status_code=status.HTTP_200_OK)
@requires_role(["admin"])
async def delete_date(
    date_id: int,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    result = await crud.delete(model=Date, session=db, id=date_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Date not found"
        )
    return {"detail": "Date deleted successfully"}
