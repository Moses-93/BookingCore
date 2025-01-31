import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime

from core.dependencies import get_db, verify_user
from decorators.permissions import requires_role
from schemas import booking
from db.models import Booking, User
from db.crud import crud
from utils.validators import ensure_resource_exists, check_number_masters


router = APIRouter(prefix="/bookings", tags=["bookings"])
logger = logging.getLogger(__name__)


@router.get(
    "/", response_model=List[booking.BookingResponse], status_code=status.HTTP_200_OK
)
@requires_role(["master", "user", "admin"])
async def get_booking(
    active: bool | None = Query(None),
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    filters = {"active": active} if active is not None else {}

    if user.role == "master":
        filters["master_id"] = user.id
    else:
        filters["user_id"] = user.id

    result = await crud.read(model=Booking, session=db, **filters)

    bookings = await result.scalars().all()
    ensure_resource_exists(bookings)
    return bookings


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["admin", "user"])
async def create_booking(
    booking: booking.BookingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
    master_id: int | None = Query(None),
):
    if not master_id:
        master = check_number_masters(user)
        master_id = master.id
    result = await crud.create(
        model=Booking,
        session=db,
        time=datetime.strptime(booking.time, "%H:%M").time(),
        user_id=user.id,
        service_id=booking.service_id,
        date_id=booking.date_id,
        time_id=booking.time_id,
        master_id=master_id,
    )
    ensure_resource_exists(result, status_code=400, message="Failed to create booking")
    return result
