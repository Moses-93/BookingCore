import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from datetime import datetime, timedelta
from typing import Optional

from core.constants import PAYMENT_MESSAGE

from db.models import subscription as s
from db.crud import new_crud
from utils.validators import ensure_resource_exists
from .notifications import NotificationService, notification_service


logger = logging.getLogger(__name__)


class SubscriptionPlanService:

    async def get_plans(self, session: AsyncSession) -> Optional[s.SubscriptionPlan]:
        subscription = await new_crud.read(
            select(s.SubscriptionPlan).order_by("price"), session
        )
        ensure_resource_exists(subscription)
        return subscription.scalars().all()

    async def get_plan(
        self, session: AsyncSession, plan_id
    ) -> Optional[s.SubscriptionPlan]:
        plan = await session.get(s.SubscriptionPlan, plan_id)
        ensure_resource_exists(plan)
        return plan


class SubscriptionService:

    def __init__(
        self,
        notification_manager: NotificationService,
        subscription_plan_manager: SubscriptionPlanService,
    ):
        self.notification_manager = notification_manager
        self.subscription_plan_manager = subscription_plan_manager

    async def get_subscription(
        self, session: AsyncSession, user_id: int
    ) -> Optional[s.Subscription]:
        result = await new_crud.read(
            select(s.Subscription).filter_by(master_id=user_id), session
        )
        subscription = result.scalar()
        ensure_resource_exists(subscription)
        return subscription

    async def calculate_end_date(self, duration_days: int) -> datetime:
        return datetime.now() + timedelta(days=duration_days)

    async def create_subscription(
        self, session: AsyncSession, user_id: int, plan_id: int, chat_id: int
    ) -> Optional[s.Subscription]:
        logger.info("Створення підписки")
        plan = await self.subscription_plan_manager.get_plan(session, plan_id)
        end_date = await self.calculate_end_date(plan.duration_days)
        subscription = s.Subscription(
            master_id=user_id, plan_id=plan.id, end_date=end_date
        )
        created_subscription = await new_crud.create(subscription, session)

        if created_subscription:
            logger.info("Підписка створена успішно")
            await self.notification_manager.send_message(
                chat_id, PAYMENT_MESSAGE["success_active_subscription"]
            )
        else:
            logger.error(
                f"Помилка при створенні підписки. Вхідні дані: user_id: {user_id} | plan_id: {plan_id}"
            )
            await self.notification_manager.send_message(
                chat_id, PAYMENT_MESSAGE["error_activation_subscription"]
            )

        return created_subscription


subscription_plan_service = SubscriptionPlanService()
subscription_service = SubscriptionService(
    notification_service, subscription_plan_service
)
