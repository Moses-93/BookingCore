import logging
from fastapi import APIRouter
from src.api.v1.handler_factory import HandlerFactory
from src.api.v1.endpoints import (
    ServiceRouter,
    BookingRouter,
    UserRouter,
    PaymentRouter,
    FeedbackRouter,
    ScheduleRouter,
    BusinessInfoRouter,
    SubscriptionRouter,
)

logger = logging.getLogger(__name__)


class APIFactory:
    def __init__(self, handlers: HandlerFactory):
        logger.info(f"Call __init__ APIFactory for an instance {self}")
        self.handlers = handlers

    def create_service_router(self):
        return ServiceRouter(self.handlers.create_service_handler())

    def create_booking_router(self):
        return BookingRouter(self.handlers.create_booking_handler())

    def create_user_router(self):
        return UserRouter(self.handlers.create_user_handler())

    def create_payment_router(self):
        return PaymentRouter(self.handlers.create_payment_handler())

    def create_feedback_router(self):
        return FeedbackRouter(self.handlers.create_feedback_handler())

    def create_schedule_router(self):
        return ScheduleRouter(self.handlers.create_schedule_handler())

    def create_business_info_router(self):
        return BusinessInfoRouter(self.handlers.create_business_info_handler())

    def create_subscription_router(self):
        return SubscriptionRouter(self.handlers.create_subscription_handler())

    def create_main_v1_router(self):

        main_v1_router = APIRouter()

        routers = [
            self.create_booking_router(),
            self.create_business_info_router(),
            self.create_feedback_router(),
            self.create_payment_router(),
            self.create_schedule_router(),
            self.create_service_router(),
            self.create_subscription_router(),
            self.create_user_router()
        ]
        for router in routers:
            main_v1_router.include_router(router.router)
        
        return main_v1_router
