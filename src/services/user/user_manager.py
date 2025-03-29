import logging
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserCreate
from src.services.user import UserService
from src.db.models import User

logger = logging.getLogger(__name__)


class UserManager:

    def __init__(self, user_service: UserService):
        logger.info(f"Call __init__ UserManager for an instance {self}")
        self.user_service = user_service

    async def create_user(self, session: AsyncSession, user_data: UserCreate) -> User:
        logger.info(f"Calling a manager method to create a user")
        return await self.user_service.create_user(session, user_data)

    async def delete_user(self, session: AsyncSession, user_id: int):
        await self.user_service.delete_user(session, user_id)

    async def deactivate_user(self, session: AsyncSession, user_id: int):
        await self.user_service.deactivate_user(session, user_id)

    async def add_master_to_user(
        self, session: AsyncSession, user_id: int, master_chat_id: int
    ):
        await self.user_service.add_master_to_user(session, user_id, master_chat_id)
