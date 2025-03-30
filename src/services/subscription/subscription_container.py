from dependency_injector import containers, providers
from src.db.repository import CRUDRepository
from src.services.container import create_core_container

from .subscription_service import SubscriptionService, SubscriptionPlanService
from .subscription_manager import SubscriptionManager


class SubscriptionContainer(containers.DeclarativeContainer):

    notification_service = providers.Dependency()

    subscription_plan_service = providers.Singleton(
        SubscriptionPlanService, crud_repository=CRUDRepository
    )
    subscription_service = providers.Singleton(
        SubscriptionService,
        crud_repository=CRUDRepository,
        notification_service=notification_service,
    )

    subscription_manager = providers.Singleton(
        SubscriptionManager,
        subscription_service=subscription_service,
        subscription_plan_service=subscription_plan_service,
    )


def create_subscription_container():
    core_container = create_core_container()
    return SubscriptionContainer(
        notification_service=core_container.notification_service
    )
