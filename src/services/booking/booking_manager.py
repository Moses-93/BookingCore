from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user import User
from src.schemas.booking import BookingCreate
from typing import List, Optional
from src.db.models import Booking
from src.services.booking.booking_service import (
    BookingDeactivationService,
    BookingNotificationService,
    BookingReminderService,
    BookingService,
)


class BookingManager:
    def __init__(
        self,
        booking_service: BookingService,
        booking_notification_service: BookingNotificationService,
        booking_deactivation_service: BookingDeactivationService,
        booking_reminder_service: BookingReminderService,
    ):
        self.booking_service = booking_service
        self.booking_notification_service = booking_notification_service
        self.booking_deactivation_service = booking_deactivation_service
        self.booking_reminder_service = booking_reminder_service

    async def get_bookings(
        self,
        session: AsyncSession,
        user_id: int,
        user_role: str,
        is_active: bool,
        offset: int,
        limit: int,
    ) -> List[Booking]:
        return await self.booking_service.get_bookings(
            session, user_id, user_role, is_active, offset, limit
        )

    async def create_booking(
        self,
        session: AsyncSession,
        booking_data: BookingCreate,
        user: User,
        master_id: Optional[int],
    ) -> Booking:
        if master_id is None:
            master_id = user.masters[0]
        created_booking = await self.booking_service.create_booking(
            session, booking_data, user.id, master_id
        )
        await self._update_time_slot(session, created_booking.time_id, is_active=False)
        await self._send_booking_notification(user, booking_data)

    async def deactivate_booking(
        self,
        session: AsyncSession,
        booking_id: int,
        client_name: str,
        client_chat_id: int,
    ) -> None:
        await self.booking_service.deactivate_booking(session, booking_id)
        booking = await self.booking_service.get_booking_by_id(session, booking_id)

        await self._update_time_slot(session, booking.time_id, is_active=True)

        await self._send_cancel_booking_notification(
            client_name,
            client_chat_id,
            booking.service.name,
            booking.date.date,
            booking.time.time,
        )

    async def _send_booking_notification(
        self, client: User, booking_data: BookingCreate
    ):
        msg_to_client, msg_to_master = (
            self.booking_notification_service.create_notification_message(
                client.name, client.phone_number, booking_data
            )
        )
        master = client.masters[0]
        await self.booking_notification_service.send_notification(
            client.chat_id, msg_to_client
        )
        await self.booking_notification_service.send_notification(
            master.chat_id, msg_to_master
        )

    async def _send_cancel_booking_notification(
        self, client_name, client_chat_id: int, service: str, date, time
    ):
        msg = await self.booking_notification_service.create_cancel_booking_message(
            client_name,
            service,
            date,
            time,
        )
        await self.booking_notification_service.send_notification(client_chat_id, msg)

    async def _update_time_slot(self, session: AsyncSession, time_id: int, **kwargs):
        await self.booking_deactivation_service.update_time_slot(
            session, time_id, **kwargs
        )
