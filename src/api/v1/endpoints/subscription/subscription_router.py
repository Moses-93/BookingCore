from typing import Dict, Union
from fastapi import APIRouter, status
from src.api.v1.endpoints.subscription import SubscriptionHandler


class SubscriptionRouter:
    def __init__(self, subscription_handler: SubscriptionHandler):
        self.router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])
        self._registry_router(subscription_handler)

    def _registry_router(self, handler: SubscriptionHandler):
        self.router.add_api_route(
            "/plans/",
            handler.get_subscription_plans,
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/plans/{plan_id}",
            handler.get_subscription_plan,
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/",
            handler.get_subscription,
            status_code=status.HTTP_200_OK,
            methods=["GET"],
        )
        self.router.add_api_route(
            "/activate-free-plan",
            handler.create_subscription,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
        )
        self.router.add_api_route(
            "/cancel-preview",
            handler.cancel_preview_subscription,
            status_code=status.HTTP_200_OK,
            response_model=Dict[str, Union[float, bool]],
            methods=["POST"],
        )
