import logging
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies.database import get_db
from src.core.dependencies.auth import get_current_user
from src.decorators.permissions import requires_role
from src.schemas.business_info import (
    BusinessInfoCreate,
    BusinessInfoUpdate,
)
from src.db.models.user import User

logger = logging.getLogger(__name__)


class BusinessInfoHandler:
    def __init__(self, business_info_manager):
        self.business_info_manager = business_info_manager

    @requires_role(["master", "client"])
    async def get_business_info(
        self,
        master_id: int | None = Query(None),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        business_info_data = await self.business_info_manager.get_business_info(
            db, user, master_id
        )
        logger.info(f"business_info: {business_info_data}")

        return business_info_data

    @requires_role(["master"])
    async def create_business_info(
        self,
        business_info: BusinessInfoCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        created_business_info = await self.business_info_manager.create_business_info(
            db, business_info, user.id
        )
        return created_business_info

    @requires_role(["master"])
    async def update_business_info(
        self,
        business_info: BusinessInfoUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        await self.business_info_manager.update_business_info(
            db, user.id, business_info
        )
