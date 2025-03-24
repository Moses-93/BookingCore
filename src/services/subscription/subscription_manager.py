from src.services.subscription.subscription_service import (
    SubscriptionService,
    SubscriptionPlanService,
)


class SubscriptionManager:

    def __init__(
        self,
        subscription_service: SubscriptionService,
        subscription_plan_service: SubscriptionPlanService,
    ):
        self.subscription_plan_service = subscription_plan_service
        self.subscription_service = subscription_service
