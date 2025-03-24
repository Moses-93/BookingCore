from typing import NamedTuple

from src.services.booking.booking_service import (
    BookingDeactivationService,
    BookingNotificationService,
    BookingReminderService,
    BookingService,
)
from src.services.schedule.date_service import DateScheduleService
from src.services.schedule.time_service import TimeScheduleService
from src.services.subscription import SubscriptionPlanService, SubscriptionService


class BookingServices(NamedTuple):
    service: BookingService
    deactivation_service: BookingDeactivationService
    notification_service: BookingNotificationService
    reminder_service: BookingReminderService


class ScheduleServices(NamedTuple):
    time_service: TimeScheduleService
    date_service: DateScheduleService


class SubscriptionServices(NamedTuple):
    plan_service: SubscriptionPlanService
    subscription_service: SubscriptionService
