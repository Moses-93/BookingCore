import logging
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.dependencies import get_db, get_current_user
from decorators.permissions import requires_role
from schemas import booking
from db.models.booking import Booking
from db.models.user import User
from db.repository import crud
from services.booking import booking_service
from services.user.user_service import user_tools
from utils.validators import ensure_resource_exists


router = APIRouter(prefix="/bookings", tags=["bookings"])
logger = logging.getLogger(__name__)


@router.get("/", status_code=status.HTTP_200_OK)
@requires_role(["master", "client", "master"])
async def get_bookings(
    is_active: bool | None = Query(None),
    limit: int = Query(default=5, ge=1, le=50),
    offset: int = Query(default=0),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    filters = {"is_active": is_active} if is_active is not None else {}
    if user.role == "master":
        filters["master_id"] = user.id
    filters["user_id"] = user.id
    bookings = await booking_service.get_bookings(db, filters, offset, limit)
    return bookings


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["master", "client"])
async def create_booking(
    booking: booking.BookingCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    master_id: int | None = Query(None),
):
    if not master_id:
        master = user_tools.check_number_masters(user)
        master_id = master.id

    new_booking = await booking_service.create_booking(db, booking, user, master_id)
    return new_booking


@router.patch("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["client"])
async def deactivate_book(
    booking_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await crud.update(
        model=Booking,
        session=db,
        expressions=(Booking.id == booking_id,),
        is_active=False,
    )
    ensure_resource_exists(result)
