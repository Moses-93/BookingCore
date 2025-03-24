import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import date, time, datetime
from typing import List, Tuple
from db.models import Booking, Time
from schemas.booking import BookingCreate
from utils.validators import ensure_resource_exists
from tasks.reminders import BookingReminderTask
from tasks.deactivation import DeactivateBookingTask
from services.notifications import NotificationService
from services.user import UserService
from utils.encryption import encryption_service
from db.repository import CRUDRepository

REMINDER_MESSAGES = {
    "msg_to_master": "🚀 {master_name}, у тебе запис: {client_name} на {service} – {date}, {time}. Готуйся до роботи! 💼✨",
    "msg_to_client": "🌟 Привіт, {name}! Нагадуємо про твій запис на {service} – {date}, {time}.\nМи вже готуємося до твого візиту! Якщо щось зміниться, будь ласка, повідом нас. 😊 До зустрічі!",
}

BOOKING_MESSAGES = {
    "msg_to_master": "📅 У вас новий запис!\n\n"
    "👤 Ім'я: {name}\n"
    "💼 Послуга: {service}\n"
    "📅 Дата: {date}\n"
    "⏰ Час: {time}\n"
    "📞 Номер телефону: {phone_number}\n\n"
    "Будь готовий до зустрічі з клієнтом! 💪",
    "msg_to_client": "✅ Вітаємо, {name}!\n\n"
    "Ви успішно записались на послугу:\n"
    "💼 {service}\n"
    "📅 Дата: {date}\n"
    "⏰ Час: {time}\n\n"
    "Ми з нетерпінням чекаємо на вас! 🎉\n"
    "Якщо щось зміниться, дайте нам знати. 😊",
    "msg_cancel_to_master": "🚨 Скасований запис!\n\n"
    "👤 Ім'я клієнта: {name}\n"
    "💼 Послуга: {service}\n"
    "📅 Дата: {date}\n"
    "⏰ Час: {time}",
}

logger = logging.getLogger(__name__)


class BookingNotificationService:

    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def create_reminder_message(
        self,
        client_name: str,
        master_name: str,
        booking_data: BookingCreate,
    ) -> Tuple[str]:
        """Create a reminder message."""
        return REMINDER_MESSAGES["msg_to_client"].format(
            name=client_name,
            service=booking_data.service,
            date=booking_data.date,
            time=booking_data.time,
        ), REMINDER_MESSAGES["msg_to_master"].format(
            master_name=master_name,
            client_name=client_name,
            service=booking_data.service,
            date=booking_data.date,
            time=booking_data.time,
        )

    def create_cancel_booking_message(self, name: str, service: str, date, time) -> str:
        return BOOKING_MESSAGES["msg_cancel_to_master"].format(
            name=name, service=service, date=date, time=time
        )

    def create_notification_message(
        self,
        client_name: str,
        client_phone_number: str,
        booking_data: BookingCreate,
    ) -> Tuple[str]:
        """Create a notification message."""
        return BOOKING_MESSAGES["msg_to_master"].format(
            name=client_name,
            service=booking_data.service,
            date=booking_data.date,
            time=booking_data.time,
            phone_number=encryption_service.decrypt(client_phone_number),
        ), BOOKING_MESSAGES["msg_to_client"].format(
            name=client_name,
            service=booking_data.service,
            date=booking_data.date,
            time=booking_data.time,
        )

    async def send_notification(self, chat_id: int, message: str):
        """Send a notification to a user."""
        await self.notification_service.send_message(chat_id, message)


class BookingDeactivationService:

    def __init__(
        self, crud_repository: CRUDRepository, deactivation_task: DeactivateBookingTask
    ):
        self.crud_repository = crud_repository
        self.deactivation_task = deactivation_task

    async def schedule_deactivate_booking(
        self, booking_id: int, date: date, time: time
    ):
        logger.info("Launch scheduler to deactivate booking")
        deactivate_time = datetime.combine(date, time)
        delay = (deactivate_time - datetime.now()).total_seconds()
        self.deactivation_task.deactivate_booking.apply_async(
            args=[booking_id], countdown=int(delay)
        )

    async def update_time_slot(self, session: AsyncSession, time_id: int, **kwargs):
        """Update a time slot for a booking."""
        await self.crud_repository.update(
            update(Time).filter_by(id=time_id).values(**kwargs), session
        )


class BookingReminderService:

    def __init__(self, booking_reminder_task: BookingReminderTask):
        self.booking_reminder_task = booking_reminder_task

    async def schedule_reminder(
        self, chat_id: int, reminder_time: datetime, message: str
    ):
        logger.info("Launch scheduler to send reminder")
        delay = (reminder_time - datetime.now()).total_seconds()

        if delay <= 0:
            logger.warning(
                f"The reminder for {chat_id} has an expired value of {reminder_time}."
            )
            return

        self.booking_reminder_task.send_booking_reminder.apply_async(
            args=[chat_id, message], countdown=int(delay)
        )
        logger.info(f"Reminder is scheduled for {chat_id} in {delay} seconds.")


class BookingService:

    def __init__(self, crud_repository: CRUDRepository):
        self.crud_repository = crud_repository

    async def get_booking_by_id(
        self, session: AsyncSession, booking_id: int
    ) -> Booking:
        return await session.get(Booking, booking_id)

    async def get_bookings(
        self,
        session: AsyncSession,
        user_id: int,
        user_role: str,
        is_active: bool,
        offset: int,
        limit: int,
    ) -> List[Booking]:
        """Retrieve bookings based on filters, offset, and limit."""
        key = "master_id" if user_role == "master" else "user_id"
        filters = {key: user_id}
        if is_active:
            filters["is_active":True]
        query = await self.crud_repository.read(
            select(Booking).filter_by(**filters).limit(limit).offset(offset), session
        )
        bookings = query.unique().scalars().all()
        ensure_resource_exists(bookings)
        return bookings

    async def create_booking(
        self,
        session: AsyncSession,
        booking_data: BookingCreate,
        user_id: int,
        master_id: int,
    ) -> Booking:
        """Create a new booking."""
        booking_dump = booking_data.model_dump(
            exclude={"date", "time", "service", "master_id"}
        )

        return await self.crud_repository.create(
            Booking(user_id=user_id, master_id=master_id, **booking_dump), session
        )

    async def deactivate_booking(self, session: AsyncSession, booking_id: int) -> bool:
        return self.crud_repository.update(
            update(Booking).where(Booking.id == booking_id).values(is_active=False),
            session,
        )
