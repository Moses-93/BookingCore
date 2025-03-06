import logging

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from core.dependencies import get_db
from db.crud import crud
from db.models.user import User
from db.models.booking import Time
from schemas.time import TimeCreate, TimeResponse
from decorators.permissions import requires_role
from utils.validators import ensure_resource_exists
from tasks.deactivate_times import schedule_deactivate_time


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/times", tags=["times"])


@router.get("/", response_model=list[TimeResponse], status_code=status.HTTP_200_OK)
@requires_role(["master", "client", "master"])
async def get_times(
    master_id: int | None = Query(None),
    date_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):

    if master_id is None:
        master = check_number_masters(user)
        master_id = master.id

    result = await crud.read(model=Time, session=db, date_id=date_id)
    times = result.unique().scalars().all()
    logger.debug(f"times for date_id {date_id}: {times}")
    ensure_resource_exists(times)
    return times


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["master", "master"])
async def create_time(
    time: TimeCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    new_time = await crud.create(
        model=Time,
        session=db,
        time=time.time,
        date_id=time.date_id,
    )
    ensure_resource_exists(new_time, status_code=400, message="Failed to create time")
    logger.info(f"Time {time.time} for date_id {time.date_id} created successfully")
    await schedule_deactivate_time(new_time.id, time.date, time.time)
    return new_time


@router.delete("/{time_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def delete_time(
    time_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await crud.delete(model=Time, session=db, id=time_id)
    logger.info(f"Time with id {time_id} deleted successfully")
    ensure_resource_exists(result)
