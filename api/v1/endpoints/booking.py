import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from core.dependencies import get_db, verify_user
from decorators.permissions import requires_role
from schemas import booking
from db.models import Booking, User
from db.crud import crud
from utils.validators import ensure_resource_exists


router = APIRouter(prefix="/bookings", tags=["bookings"])
logger = logging.getLogger(__name__)


@router.post("/")
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
    )
    ensure_resource_exists(result, status_code=400, message="Failed to create booking")
    return result
