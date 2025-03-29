import logging
from src.core.dependencies.dependency_factory import DependencyFactory
from src.api.v1.endpoints import (
    ServiceHandler,
    BookingHandler,
    ScheduleHandler,
    BusinessInfoHandler,
    FeedbackHandler,
    SubscriptionHandler,
    UserHandler,
    PaymentHandler,
)

logger = logging.getLogger(__name__)


class HandlerFactory:
    def __init__(self, deps: DependencyFactory):
        logger.info(f"Call __init__ HandlerFactory for an instance {self}")
        self.deps = deps

    def create_service_handler(self):
        return ServiceHandler(self.deps.create_service_manager())

    def create_booking_handler(self):
        return BookingHandler(self.deps.create_booking_manager())

    def create_schedule_handler(self):
        return ScheduleHandler(self.deps.create_schedule_manager())

    def create_business_info_handler(self):
        return BusinessInfoHandler(self.deps.create_business_info_manager())

    def create_feedback_handler(self):
        return FeedbackHandler(self.deps.create_feedback_manager())

    def create_subscription_handler(self):
        return SubscriptionHandler(self.deps.create_subscription_manager())

    def create_user_handler(self):
        return UserHandler(self.deps.create_user_manager())

    def create_payment_handler(self):
        return PaymentHandler(self.deps.create_wfp_manager())
