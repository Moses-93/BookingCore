import logging
from typing import Type, List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, update

from src.db.models import User
from src.db.repository import CRUDRepository
from src.services.user import UserService


logger = logging.getLogger(__name__)


class BaseScheduleService:
    def __init__(
        self,
        crud_repository: CRUDRepository,
        user_service: UserService,
        model: Type[DeclarativeBase],
    ):
        self.crud_repository = crud_repository
        self.user_service = user_service
        self.model = model

    async def create(
        self, session: AsyncSession, user_id: int, data: Dict[str, Any]
    ) -> Optional[Type[DeclarativeBase]]:
        data["master_id"] = user_id
        stmt = self.model(**data)
        return await self.crud_repository.create(stmt, session)

    async def get_all(
        self, session: AsyncSession, user: User, master_id: int
    ) -> Optional[List[DeclarativeBase]]:
        filters = {}
        if not master_id:
            filters = await self.user_service.identify_role(user, filters)
        result = await self.crud_repository.read(
            select(self.model).filter_by(is_active=True, **filters), session
        )
        return result.unique().scalars().all()

    async def get_one(
        self, session: AsyncSession, obj_id: int
    ) -> Optional[DeclarativeBase]:
        return await session.get(self.model, obj_id)

    async def deactivate(self, session: AsyncSession, obj_id: int) -> bool:
        return await self.crud_repository.update(
            update(self.model).where(self.model.id == obj_id).values(is_active=False),
            session,
        )
