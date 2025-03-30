from dependency_injector import containers, providers

from . import booking_service as b_s
from .booking_manager import BookingManager
from src.services.container import create_core_container
from src.db.repository import CRUDRepository


class BookingContainer(containers.DeclarativeContainer):

    notification_service = providers.Dependency()
    booking_service = providers.Singleton(
        b_s.BookingService,
        crud_repository=CRUDRepository,
    )
    booking_notification_service = providers.Singleton(
        b_s.BookingNotificationService,
        notification_service=notification_service,
    )
    booking_deactivation_service = providers.Singleton(
        b_s.BookingDeactivationService,
        crud_repository=CRUDRepository,
    )
    booking_reminder_service = providers.Singleton(
        b_s.BookingReminderService,
    )
    booking_manager = providers.Singleton(
        BookingManager,
        booking_service=booking_service,
        booking_notification_service=booking_notification_service,
        booking_deactivation_service=booking_deactivation_service,
        booking_reminder_service=booking_reminder_service,
    )


def create_booking_container() -> BookingContainer:
    core_container = create_core_container()
    return BookingContainer(notification_service=core_container.notification_service())
