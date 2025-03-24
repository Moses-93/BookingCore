from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from services.service.service_repository import ServiceRepository
from schemas import ServiceCreate, ServiceUpdate


class ServiceManager:

    def __init__(self, service_repository: ServiceRepository):
        self.service_repository = service_repository

    async def get_services(self, session: AsyncSession, user: User, master_id):
        return await self.service_repository.get_services(session, user, master_id)

    async def create_service(
        self, session: AsyncSession, service_data: ServiceCreate, master_id: int
    ):

        return await self.service_repository.create_service(
            session, service_data, master_id
        )

    async def update_service(
        self, session: AsyncSession, service_data: ServiceUpdate, service_id: int
    ):
        update_service = service_data.model_dump(exclude_unset=True)
        await self.service_repository.update_service(
            session, service_id, **update_service
        )

    async def deactivate_service(self, session: AsyncSession, service_id: int):
        await self.service_repository.update_service(
            session, service_id, is_active=False
        )
