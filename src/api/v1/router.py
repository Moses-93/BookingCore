from fastapi import APIRouter
from api.v1.api_factory import APIFactory


def create_main_router() -> APIRouter:

    main_v1_router = APIRouter()

    api_factory = APIFactory()

    main_v1_router.include_router(api_factory.create_service_router().router)
    main_v1_router.include_router(api_factory.create_booking_router().router)
    main_v1_router.include_router(api_factory.create_business_info_router().router)
    main_v1_router.include_router(api_factory.create_feedback_router().router)
    main_v1_router.include_router(api_factory.create_payment_router().router)
    main_v1_router.include_router(api_factory.create_schedule_router().router)
    main_v1_router.include_router(api_factory.create_subscription_router().router)
    main_v1_router.include_router(api_factory.create_user_router().router)

    return main_v1_router
