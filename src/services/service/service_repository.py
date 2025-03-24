from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from db.repository import CRUDRepository
from db.models import Service, User
from schemas import ServiceCreate

from utils.redis_cache import RedisCacheFactory
from services.user import UserService


class ServiceRepository:
    def __init__(
        self,
        crud_repository: CRUDRepository,
        user_service: UserService,
        redis_cache: RedisCacheFactory,
    ):
        self.crud_repository = crud_repository
        self.user_service = user_service
        self.cache = redis_cache

    async def get_services(
        self, session: AsyncSession, user: User, master_id: Optional[int]
    ) -> List[Service]:
        filters = {"is_active": True, "master_id": master_id}
        if user.role == "master":
            filters["master_id"] = user.id
        if master_id is None:
            master = await self.user_service.check_number_masters(user)
            filters["master_id"] = master.id

        return await self.crud_repository.read(
            select(Service).filter_by(**filters), session
        )

    async def create_service(
        self, session: AsyncSession, service_data: ServiceCreate, master_id: int
    ) -> Service:
        dump = service_data.model_dump()
        dump["master_id"] = master_id
        return await self.crud_repository.create(Service(**dump), session)

    async def update_service(self, session: AsyncSession, service_id: int, **values):
        return await self.crud_repository.update(
            update(Service).where(Service.id == service_id).values(**values), session
        )
