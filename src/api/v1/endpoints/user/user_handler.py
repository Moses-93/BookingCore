import logging
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies.auth import get_db, get_current_user
from src.decorators.permissions import requires_role
from src.schemas.user import UserCreate, MasterLinkRequest
from src.db.models.user import User
from src.services.user.user_manager import UserManager

logger = logging.getLogger(__name__)


class UserHandler:

    def __init__(self, user_manager: UserManager):
        logger.info(f"Call __init__ UserHandler for an instance {self}")
        self.user_manager = user_manager

    @requires_role(["admin", "master", "client"])
    async def get_user(self, user: User = Depends(get_current_user)):
        logger.info(f"User: {user}")
        return user

    async def create_user(
        self,
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db),
    ):
        return await self.user_manager.create_user(db, user_data)

    async def link_master_to_user(
        self,
        master: MasterLinkRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        await self.user_manager.add_master_to_user(db, user.id, master.master_chat_id)

    @requires_role(["client", "master"])
    async def delete_user(
        self,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        await self.user_manager.delete_user(db, user.id)
