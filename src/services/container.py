from dependency_injector import containers, providers
from src.db.repository import CRUDRepository
from .notifications import NotificationService
from .user import user_service


class CoreContainer(containers.DeclarativeContainer):
    notification_service = providers.Singleton(NotificationService)
    user_service = providers.Singleton(
        user_service.UserService, crud_repository=CRUDRepository
    )


def create_core_container():
    return CoreContainer()
