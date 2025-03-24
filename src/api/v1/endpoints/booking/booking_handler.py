import logging
from typing import Optional
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies.database import get_db
from src.core.dependencies.auth import get_current_user
from src.db.models import User
from src.decorators.permissions import requires_role
from src.schemas import BookingCreate
from src.services.booking import BookingManager

logger = logging.getLogger(__name__)


class BookingHandler:

    def __init__(self, booking_manager: BookingManager):
        self.booking_manager = booking_manager

    @requires_role(["master", "client"])
    async def get_bookings(
        self,
        is_active: bool | None = Query(None),
        limit: int = Query(default=5, ge=1, le=50),
        offset: int = Query(default=0),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):

        return await self.booking_manager.get_bookings(
            db, user.id, user.role, is_active, offset, limit
        )

    @requires_role(["master", "client"])
    async def create_booking(
        self,
        booking: BookingCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
        master_id: Optional[int] = Query(None),
    ):
        return await self.booking_manager.create_booking(db, booking, user, master_id)

    @requires_role(["client"])
    async def deactivate_book(
        self,
        booking_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        await self.booking_manager.deactivate_booking(
            db, booking_id, user.name, user.chat_id
        )
