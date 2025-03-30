from src.services.container import create_core_container
from src.services.booking.booking_container import create_booking_container
from src.services.business_info.business_info_container import (
    create_business_info_container,
)
from src.services.feedback.feedback_container import create_feedback_container
from src.services.payments.payment_container import create_payment_container
from src.services.schedule.schedule_container import create_schedule_container
from src.services.service.service_container import create_service_container
from src.services.subscription.subscription_container import create_subscription_container
from src.services.payments.wayforpay.wayforpay_factory import create_wfp_manager
from src.services.user.user_manager import UserManager



class DependencyFactory:
    def __init__(self):
        self.core_container = create_core_container()
        self.booking_container = create_booking_container()
        self.schedule_container = create_schedule_container()
        self.service_container = create_service_container()
        self.subscription_container = create_subscription_container()
        self.feedback_container = create_feedback_container()
        self.business_info_container = create_business_info_container()
        self.payment_container = create_payment_container()

    def get_booking_manager(self):
        return self.booking_container.booking_manager()

    def get_schedule_manager(self):
        return self.schedule_container.schedule_manager()

    def get_service_manager(self):
        return self.service_container.service_manager()

    def get_sub_manager(self):
        return self.subscription_container.subscription_manager()

    def get_user_manager(self):
        return UserManager(self.core_container.user_service())

    def get_wfp_manager(self):
        return create_wfp_manager(self.payment_container.payment_service())

    def get_feedback_manager(self):
        return self.feedback_container.feedback_manager()

    def get_business_info_manager(self):
        return self.business_info_container.business_info_manager()
