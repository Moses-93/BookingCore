from dependency_injector import containers, providers
from src.db.repository import CRUDRepository
from src.services.container import create_core_container
from .service_repository import ServiceRepository
from .service_manager import ServiceManager


class ServiceContainer(containers.DeclarativeContainer):
    user_service = providers.Dependency()
    service_repository = providers.Singleton(
        ServiceRepository, crud_repository=CRUDRepository, user_service=user_service
    )
    service_manager = providers.Singleton(
        ServiceManager, service_repository=service_repository
    )


def create_service_container():
    core_container = create_core_container()
    return ServiceContainer(user_service=core_container.user_service)
