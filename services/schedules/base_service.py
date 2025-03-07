import logging
from typing import Type, List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, update

from db.models.user import User
from db.crud import new_crud
from services.user import UserTools


logger = logging.getLogger(__name__)

class BaseScheduleService:
    def __init__(self, user_tools: UserTools, model: Type[DeclarativeBase]):
        self.user_tools = user_tools
        self.model = model

    async def create(self, session: AsyncSession, user_id: int, data: Dict[str, Any]) -> Optional[Type[DeclarativeBase]]:
        data["master_id"] = user_id
        stmt = self.model(**data)
        created_obj = await new_crud.create(stmt, session)
        return created_obj

    async def get_all(
        self, session: AsyncSession, user: User, master_id: int
    ) -> Optional[List[DeclarativeBase]]:
        filters = {}
        if not master_id:
            filters = await self.user_tools.identify_role(user, filters)
        result = await new_crud.read(
            select(self.model).filter_by(is_active=True, **filters), session
        )
        objs = result.unique().scalars().all()
        return objs

    async def get_one(self, session: AsyncSession, obj_id: int) -> Optional[DeclarativeBase]:
        return await session.get(self.model, obj_id)

    async def deactivate(self, session: AsyncSession, obj_id: int) -> bool:
        return await new_crud.update(
            update(self.model).where(self.model.id == obj_id).values(is_active=False),
            session,
        )
    