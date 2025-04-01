from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User
from src.services.service.service_handler import ServiceHandler
from src.schemas import ServiceCreate, ServiceUpdate


class ServiceManager:

    def __init__(self, service_handler: ServiceHandler):
        self.service_handler = service_handler

    async def get_services(self, session: AsyncSession, user: User, master_id):
        return await self.service_handler.get_services(session, user, master_id)

    async def create_service(
        self, session: AsyncSession, service_data: ServiceCreate, master_id: int
    ):

        return await self.service_handler.create_service(
            session, service_data, master_id
        )

    async def update_service(
        self, session: AsyncSession, service_data: ServiceUpdate, service_id: int
    ):
        update_service = service_data.model_dump(exclude_unset=True)
        await self.service_handler.update_service(
            session, service_id, **update_service
        )

    async def deactivate_service(self, session: AsyncSession, service_id: int):
        await self.service_handler.update_service(
            session, service_id, is_active=False
        )
