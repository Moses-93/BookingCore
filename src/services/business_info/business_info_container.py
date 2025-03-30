from dependency_injector import containers, providers
from src.db.repository import CRUDRepository
from .business_info_service import BusinessInfoService
from .business_info_manager import BusinessInfoManager


class BusinessInfoContainer(containers.DeclarativeContainer):
    business_info_service = providers.Singleton(
        BusinessInfoService, crud_repository=CRUDRepository
    )
    business_info_manager = providers.Singleton(
        BusinessInfoManager, business_info_service=business_info_service
    )


def create_business_info_container():
    return BusinessInfoContainer()
