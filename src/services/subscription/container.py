from typing import NamedTuple
from services.subscription import SubscriptionPlanService, SubscriptionService


class ContainerSubscriptionServices(NamedTuple):
    plan_service: SubscriptionPlanService
    subscription_service: SubscriptionService
