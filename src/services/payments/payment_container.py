from dependency_injector import containers, providers
from src.db.repository import CRUDRepository
from src.services.container import create_core_container
from src.services.subscription.subscription_container import (
    create_subscription_container,
)
from .payment_service import PaymentService


class PaymentContainer(containers.DeclarativeContainer):
    """Контейнер для сервісів оплати"""

    notification_service = providers.Dependency()
    subscription_service = providers.Dependency()

    payment_service = providers.Singleton(
        PaymentService,
        crud_repository=CRUDRepository,
        subscription_service=subscription_service,
        notification_service=notification_service,
    )


def create_payment_container():
    """Фабрика контейнера PaymentContainer"""

    core_container = create_core_container()
    sub_container = create_subscription_container()

    return PaymentContainer(
        notification_service=core_container.notification_service,
        subscription_service=sub_container.subscription_service,
    )
