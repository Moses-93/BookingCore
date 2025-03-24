from typing import NamedTuple

from services.booking.booking_service import (
    BookingDeactivationService,
    BookingNotificationService,
    BookingReminderService,
    BookingService,
)


class BookingServices(NamedTuple):
    service: BookingService
    deactivation_service: BookingDeactivationService
    notification_service: BookingNotificationService
    reminder_service: BookingReminderService
