import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies.auth import get_db, get_current_user
from src.db.models.user import User
from src.core.dependencies.auth import requires_role
from src.schemas import subscription as s

logger = logging.getLogger(__name__)


class SubscriptionHandler:

    def __init__(self, subscription_manager):
        self.subscription_manager = subscription_manager

    @requires_role(["master"])
    async def get_subscription_plans(
        self, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
    ):
        return await self.subscription_manager.get_plans(db)

    @requires_role(["master"])
    async def get_subscription_plan(
        self,
        plan_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        return await self.subscription_manager.get_plan(db, plan_id)

    @requires_role(["master"])
    async def get_subscription(
        self, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
    ):
        return await self.subscription_manager.get_subscription(db, user.id)

    @requires_role(["master"])
    async def create_subscription(
        self,
        plan: s.SubscriptionActivate,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        logger.info(f"plan:{plan}")

        await self.subscription_manager.create_subscription(db, user.id, plan.id)

    @requires_role(["master"])
    async def cancel_preview_subscription(
        self,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        logger.info("Launch the handler to cancel preview subscription")
        return await self.subscription_manager.cancel_preview_subscription(db, user.id)
