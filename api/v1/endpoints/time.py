import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import time
from core.dependencies import verify_user
from core.dependencies import get_db
from db.crud import crud
from db.models import User, Time
from schemas import time as schema_time
from decorators.permissions import requires_role

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/times", tags=["times"])


@router.get("/{date_id}", response_model=list[schema_time.TimeResponse])
@requires_role(["admin", "user"])
async def get_times(
    date_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    times = await crud.read(model=Time, session=db, date_id=date_id)
    logger.debug(f"times for date_id {date_id}: {times}")
    if not times:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Times not found for this date",
        )
    return times


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["admin"])
async def create_time(
    schema_time: schema_time.TimeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):

    new_time = await crud.create(
        model=Time,
        session=db,
        time=schema_time.time,
        date_id=schema_time.date_id,
    )
    if not new_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create time",
        )
    return new_time


@router.delete("/{time_id}/{date_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_time(
    time_id: int,
    date_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    result = await crud.delete(model=Time, session=db, id=time_id, date_id=date_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Time not found for this date",
        )
    return {"detail": "Time deleted successfully"}
