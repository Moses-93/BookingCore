import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import verify_user
from core.dependencies import get_db
from db.crud import crud
from db.models import User, Time
from schemas.time import TimeCreate, TimeResponse
from decorators.permissions import requires_role
from utils.validators import ensure_resource_exists


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/times", tags=["times"])


@router.get(
    "/{date_id}", response_model=list[TimeResponse], status_code=status.HTTP_200_OK
)
@requires_role(["admin", "user"])
async def get_times(
    date_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    result = await crud.read(model=Time, session=db, date_id=date_id)
    logger.debug(f"times for date_id {date_id}: {result}")
    ensure_resource_exists(result)
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["admin"])
async def create_time(
    time: TimeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):

    result = await crud.create(
        model=Time,
        session=db,
        time=time.time,
        date_id=time.date_id,
    )
    ensure_resource_exists(result, status_code=400, message="Failed to create time")
    logger.info(f"Time {time.time} for date_id {time.date_id} created successfully")
    return result


@router.delete("/{time_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["admin"])
async def delete_time(
    time_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    result = await crud.delete(model=Time, session=db, id=time_id)
    logger.info(f"Time with id {time_id} deleted successfully")
    ensure_resource_exists(result)
