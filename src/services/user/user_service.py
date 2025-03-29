import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update
from typing import Any, Dict, Optional
from src.db.repository import CRUDRepository
from src.db.models.user import User, user_master_association
from src.schemas.user import UserCreate


logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, crud_repository: CRUDRepository):
        logger.info(f"Call __init__ UserService for an instance {self}")
        self.crud_repository = crud_repository

    async def get_user(self, session: AsyncSession, filters: Dict):
        query = select(User).filter_by(**filters)
        user = await self.crud_repository.read(query, session)
        return user.scalar()

    async def get_user_by_id(
        self, session: AsyncSession, master_id: int
    ) -> Optional[User]:
        """Retrieve the master by ID."""
        return await session.get(User, master_id)

    async def add_master_to_user(
        self, session: AsyncSession, user_id: int, master_chat_id: int
    ):
        master = await self.get_user({"chat_id": master_chat_id})
        stmt = insert(user_master_association).values(
            user_id=user_id, master_id=master.id
        )
        await session.execute(stmt)
        await session.commit()
        logger.info(f"Master add to user successfully")

    async def create_user(self, session: AsyncSession, user_data: UserCreate):
        logger.info(f"Calling a service method to create a user")
        user_dump = user_data.model_dump(exclude={"master_chat_id"})
        new_user = await self.crud_repository.create(User(**user_dump), session)
        logger.info(f"User {new_user.name} created successfully")
        if user_data.master_chat_id is not None:
            await self.add_master_to_user(new_user.id, user_data.master_chat_id)
        return new_user

    async def delete_user(self, session: AsyncSession, user_id: int):
        await self.crud_repository.delete(delete(User).filter_by(id=user_id), session)

    async def deactivate_user(self, session: AsyncSession, user_id: int):
        await self.crud_repository.update(
            update(User).filter_by(id=user_id).values(is_active=False), session
        )

    async def identify_role(self, user: User, filters: Dict) -> Dict[str, str]:

        if user.role == "master":
            filters["master_id"] = user.id
        else:
            master = await self.check_number_masters(user)
            filters["master_id"] = master.id
        return filters

    async def check_number_masters(self, user: User) -> Dict[str, Any]:
        """
        Перевіряє кількість майстрів у користувача та повертає їх.

        :param user: Об'єкт користувача з відношенням до майстрів
        :return: Словник з кількістю майстрів та їх списком
        """
        masters = user.masters
        if len(masters) > 1:
            raise HTTPException(
                status_code=409,
                detail={
                    "count": len(masters),
                    "masters": [
                        {"id": master.id, "name": master.name} for master in masters
                    ],
                },
            )
        return masters[0]
