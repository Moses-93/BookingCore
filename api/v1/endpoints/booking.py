import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.dependencies import get_db, verify_user
from decorators.permissions import requires_role
from schemas import booking
from db.models import Booking, Master, User
from db.crud import crud
from utils.validators import ensure_resource_exists, check_number_masters
from tasks.reminders import schedule_reminder


router = APIRouter(prefix="/bookings", tags=["bookings"])
logger = logging.getLogger(__name__)


@router.get(
    "/", response_model=List[booking.BookingResponse], status_code=status.HTTP_200_OK
)
@requires_role(["master", "user", "admin"])
async def get_bookings(
    active: bool | None = Query(None),
    limit: int = Query(default=5, ge=1, le=50),
    offset: int = Query(default=0, le=0),
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    filters = {"active": active} if active is not None else {}
    if user.role == "master":
        result = await crud.read(model=Master, session=db, user_id=user.id)
        master = result.unique().scalar_one_or_none()
        filters["master_id"] = master.id
    elif user.role == "user":
        filters["user_id"] = user.id

    result = await crud.read(
        model=Booking, session=db, limit=limit, offset=offset, **filters
    )

    bookings = result.unique().scalars().all()
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
        user_id=user.id,
        service_id=booking.service_id,
        date_id=booking.date_id,
        time_id=booking.time_id,
        master_id=master_id,
        reminder_time=booking.reminder_time,
    )
    ensure_resource_exists(result, status_code=400, message="Failed to create booking")
    if booking.reminder_time:
        schedule_reminder(
            user.chat_id,
            booking.service,
            booking.date,
            booking.time,
            booking.reminder_time,
        )
    return result


@router.patch("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["user"])
async def deactivate_book(
    book_id: int, user: User = Depends(verify_user), db: AsyncSession = Depends(get_db)
):
    result = await crud.update(
        model=Booking, session=db, expressions=(Booking.id == book_id,), active=False
    )
    ensure_resource_exists(result)
