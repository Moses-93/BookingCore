import logging
from src.db.repository import CRUDRepository
from src.services.booking.booking_service import (
    BookingDeactivationService,
    BookingNotificationService,
    BookingReminderService,
    BookingService,
)
from src.services.business_info.business_info_service import BusinessInfoService
from src.services.schedule.date_service import DateScheduleService
from src.services.schedule.schedule_manager import ScheduleManager
from src.services.schedule.time_service import TimeScheduleService
from src.utils.redis_cache import RedisCacheFactory
from src.tasks.deactivation import (
    DeactivateBookingTask,
    DeactivateDateTask,
    DeactivateTimeTask,
)
from src.tasks.reminders import BookingReminderTask
from src.services.notifications import NotificationService
from src.services.service import ServiceManager, ServiceRepository
from src.services.user import UserService, UserManager
from src.services.payments.payment_service import PaymentService
from src.services.payments.wayforpay.wayforpay_factory import (
    WayForPayManager,
    create_wfp_manager,
)
from src.services.feedback import FeedbackManager, FeedbackService
from src.services.booking import (
    BookingManager,
)
from src.services.business_info import BusinessInfoManager
from src.services.subscription import (
    SubscriptionManager,
    SubscriptionService,
    SubscriptionPlanService,
)
from src.services.container import (
    BookingServices,
    ScheduleServices,
    SubscriptionServices,
)


logger = logging.getLogger(__name__)


class DependencyFactory:

    def __del__(self):
        logger.info(f"Delete instance a factory: {self}")

    def __init__(self):
        logger.info(f"Call __init__ DependencyFactory for an instance {self}")
        self.crud_repository = CRUDRepository()
        self.user_service = UserService(self.crud_repository)
        self.redis_cache = RedisCacheFactory()
        self.notification_service = NotificationService()

        self.booking_service = self.create_booking_service()
        self.payment_service = self.create_payment_service()  
        self.subscription_service = self.create_subscription_service()
        self.schedule_service = self.create_schedule_service()
        self.feedback_service = self.create_feedback_service()
        self.business_info_service = self.create_business_info_service()

    def create_user_manager(self) -> UserManager:
        return UserManager(self.user_service)

    def create_wfp_manager(self) -> WayForPayManager:
        return create_wfp_manager(self.payment_service)

    def create_service_repository(self) -> ServiceRepository:
        return ServiceRepository(
            self.crud_repository, self.user_service, self.redis_cache
        )

    def create_service_manager(self) -> ServiceManager:
        return ServiceManager(self.create_service_repository())

    def create_business_info_service(self) -> BusinessInfoService:
        return BusinessInfoService(self.crud_repository, self.redis_cache)

    def create_business_info_manager(self) -> BusinessInfoManager:
        return BusinessInfoManager(self.business_info_service)

    def create_feedback_service(self) -> FeedbackService:
        return FeedbackService(self.crud_repository)

    def create_feedback_manager(self) -> FeedbackManager:
        return FeedbackManager(self.feedback_service)

    def create_booking_service(self) -> BookingServices:
        return BookingServices(
            BookingService(self.crud_repository),
            BookingDeactivationService(
                self.crud_repository, DeactivateBookingTask(self.crud_repository)
            ),
            BookingNotificationService(self.notification_service),
            BookingReminderService(BookingReminderTask(self.notification_service)),
        )

    def create_booking_manager(self) -> BookingManager:
        
        return BookingManager(
            self.booking_service.service,
            self.booking_service.notification_service,
            self.booking_service.deactivation_service,
            self.booking_service.reminder_service,
        )

    def create_payment_service(self) -> PaymentService:
        return PaymentService(
            self.crud_repository,
            self.subscription_service,
            self.notification_service,
        )

    def create_schedule_service(self) -> ScheduleServices:
        return ScheduleServices(
            TimeScheduleService(
                self.crud_repository,
                self.user_service, 
                DeactivateTimeTask(self.crud_repository)
            ),
            DateScheduleService(
                self.crud_repository,
                self.user_service, 
                DeactivateDateTask(self.crud_repository)
            ),
        )

    def create_schedule_manager(self):
        
        return ScheduleManager(
            self.schedule_service.date_service, self.schedule_service.time_service
            )

    def create_subscription_service(
        self,
    ) -> ContainerSubscriptionServices:
        return ContainerSubscriptionServices(
            SubscriptionPlanService(self.crud_repository, self.redis_cache),
            SubscriptionService(
                self.crud_repository, self.notification_service, self.redis_cache
            ),
        )

    def create_subscription_manager(self) -> SubscriptionManager:
        return SubscriptionManager(
            self.subscription_service.plan_service, 
            self.subscription_service.subscription_service
            )
