import logging
from src.api.v1 import endpoints
from .dependency_factory import DependencyFactory


logger = logging.getLogger(__name__)


class HandlerFactory:
    def __init__(self):
        logger.info(f"Call __init__ HandlerFactory for an instance {self}")
        self.deps = DependencyFactory()

    def create_service_handler(self):
        return endpoints.ServiceHandler(self.deps.get_service_manager())

    def create_booking_handler(self):
        return endpoints.BookingHandler(self.deps.get_booking_manager())

    def create_schedule_handler(self):
        return endpoints.ScheduleHandler(self.deps.get_schedule_manager())

    def create_business_info_handler(self):
        return endpoints.BusinessInfoHandler(self.deps.get_business_info_manager())

    def create_feedback_handler(self):
        return endpoints.FeedbackHandler(self.deps.get_feedback_manager())

    def create_subscription_handler(self):
        return endpoints.SubscriptionHandler(self.deps.get_sub_manager())

    def create_user_handler(self):
        return endpoints.UserHandler(self.deps.get_user_manager())

    def create_payment_handler(self):
        return endpoints.PaymentHandler(self.deps.get_wfp_manager())
