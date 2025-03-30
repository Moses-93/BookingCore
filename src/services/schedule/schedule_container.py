from dependency_injector import containers, providers

from src.db.repository import CRUDRepository
from src.services.container import create_core_container

from . import date_service
from . import time_service
from . import schedule_manager


class ScheduleContainer(containers.DeclarativeContainer):
    notification_service = providers.Dependency()
    user_service = providers.Dependency()

    date_service = providers.Singleton(
        date_service.DateScheduleService,
        crud_repository=CRUDRepository,
        user_service=user_service,
    )
    time_service = providers.Singleton(
        time_service.TimeScheduleService,
        crud_repository=CRUDRepository,
        user_service=user_service,
    )

    schedule_manager = providers.Singleton(
        schedule_manager.ScheduleManager,
        date_service=date_service,
        time_service=time_service,
    )


def create_schedule_container() -> ScheduleContainer:
    core_container = create_core_container()
    return ScheduleContainer(
        notification_service=core_container.notification_service,
        user_service=core_container.user_service,
    )
