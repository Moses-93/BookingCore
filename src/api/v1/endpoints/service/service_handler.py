import logging
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from decorators.permissions import requires_role
from core.dependencies import get_current_user, get_db
from db.models import User
from schemas import ServiceCreate, ServiceUpdate
from services.service import ServiceManager


logger = logging.getLogger(__name__)


class ServiceHandler:

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    @requires_role(["master", "client"])
    async def get_services(
        self,
        master_id: int | None = Query(None),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):

        return await self.service_manager.get_services(db, user, master_id)

    @requires_role(["master"])
    async def create_service(
        self,
        service_creation_data: ServiceCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):

        return await self.service_manager.create_service(
            db, service_creation_data, user.id
        )

    @requires_role(["master"])
    async def update_service(
        self,
        service_id: int,
        service_to_updated: ServiceUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        await self.service_manager.update_service(db, service_to_updated, service_id)

    @requires_role(["master"])
    async def deactivate_service(
        self,
        service_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        await self.service_manager.deactivate_service(db, service_id)
