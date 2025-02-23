import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import date, time, datetime
from typing import Dict, Optional, List
from core.constants import BOOKING_MESSAGE, REMINDER_MESSAGE
from db.models.booking import Booking, Time
from db.models.user import User
from db.crud import new_crud
from schemas.booking import BookingCreate
from utils.validators import ensure_resource_exists
from tasks.task_manager import TaskManager
from .notifications import send_message
from utils.encryption import encription_service


logger = logging.getLogger(__name__)


class BookingService:

    async def get_master(self, session: AsyncSession, master_id: int) -> Optional[User]:
        """Retrieve the master by ID."""
        master = await new_crud.read(select(User).filter_by(id=master_id), session)
        return master.scalar()

    async def _create_reminder_message(
        self, booking_data: BookingCreate, master_chat_id: int
    ) -> Dict[int, str]:
        """Create a reminder message for the master."""
        return {
            master_chat_id: REMINDER_MESSAGE["reminder_booking"].format(
                service=booking_data.service,
                date=booking_data.date,
                time=booking_data.time,
            )
        }

    async def _create_notification_message(
        self, user: User, booking_data: BookingCreate, master_chat_id: int
    ) -> Dict[int, str]:
        """Create a notification message for the master."""
        return {
            master_chat_id: BOOKING_MESSAGE["msg_to_master"].format(
                name=user.name,
                service=booking_data.service,
                date=booking_data.date,
                time=booking_data.time,
                phone_number=encription_service.decrypt(user.phone_number),
            )
        }

    async def send_notification(self, chat_id: int, message: str):
        """Send a notification to a user."""
        send_message(chat_id, message)

    async def schedule_reminder(self, data: Dict[int, str], reminder_time: datetime):
        """Schedule a reminder for a user."""
        for chat_id, message in data.items():
            await TaskManager.Reminders.reminder(chat_id, reminder_time, message)

    async def schedule_deactivate_booking(
        self, booking_id: int, date: date, time: time
    ):
        """Schedule deactivate booking."""
        await TaskManager.Deactivation.booking(booking_id, date, time)

    async def deactivate_time_slot(self, session: AsyncSession, time_id: int):
        """Deactivate a time slot for a booking."""
        await new_crud.update(
            update(Time).filter_by(id=time_id).values(is_active=False), session
        )

    async def get_bookings(
        self,
        session: AsyncSession,
        filters: Dict,
        offset: int,
        limit: int,
    ) -> List[Booking]:
        """Retrieve bookings based on filters, offset, and limit."""
        query = select(Booking).filter_by(**filters).limit(limit).offset(offset)
        result = await new_crud.read(query, session)
        bookings = result.unique().scalars().all()
        ensure_resource_exists(bookings)
        return bookings

    async def create_booking(
        self,
        session: AsyncSession,
        booking_data: BookingCreate,
        user: User,
        master_id: int,
    ) -> Booking:
        """Create a new booking."""
        booking_dump = booking_data.model_dump(
            exclude={"date", "time", "service", "master_id"}
        )

        new_booking = await new_crud.create(
            Booking(user_id=user.id, master_id=master_id, **booking_dump), session
        )

        await self.deactivate_time_slot(session, new_booking.time_id)

        await self.schedule_deactivate_booking(
            new_booking.id, booking_data.date, booking_data.time
        )

        master = await self.get_master(session, master_id)

        notification_message = await self._create_notification_message(
            user, booking_data, master.chat_id
        )
        await self.send_notification(
            master.chat_id, notification_message[master.chat_id]
        )

        reminder_message = await self._create_reminder_message(
            booking_data, master.chat_id
        )
        if booking_data.reminder_time is not None:
            await self.schedule_reminder(reminder_message, booking_data.reminder_time)

        return new_booking


booking_service = BookingService()
