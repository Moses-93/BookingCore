import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from datetime import datetime, timedelta
from typing import Optional, List

from src.core.constants import PAYMENT_MESSAGE

from src.db.models import Subscription, SubscriptionPlan
from src.db.repository import CRUDRepository
from src.utils import ensure_resource_exists, RedisCacheFactory
from src.services.notifications import NotificationService


logger = logging.getLogger(__name__)


class SubscriptionPlanService:

    def __init__(
        self, crud_repository: CRUDRepository, cache_factory: RedisCacheFactory
    ):
        self.cache = cache_factory
        self.crud_repository = crud_repository

    async def get_plans(
        self, session: AsyncSession
    ) -> Optional[List[SubscriptionPlan]]:
        key = "subscription_plans"
        cached_plans = await self.cache.get(key)
        if cached_plans:
            return cached_plans

        result = await self.crud_repository.read(
            select(SubscriptionPlan).filter_by(is_active=True).order_by("price"),
            session,
        )

        subscription = result.scalar()
        ensure_resource_exists(subscription)
        await self.cache.set(key, subscription, ttl=432000)
        return result

    async def get_plan(
        self, session: AsyncSession, plan_id
    ) -> Optional[SubscriptionPlan]:
        plan = await session.get(SubscriptionPlan, plan_id)
        ensure_resource_exists(plan)
        return plan


class SubscriptionService:

    def __init__(
        self,
        crud_repository: CRUDRepository,
        notification_service: NotificationService,
        cache: RedisCacheFactory,
    ):
        self.crud_repository = crud_repository
        self.notification_service = notification_service
        self.cache = cache

    def calculate_refund_money(
        self,
        sub_start_date: datetime,
        price: float,
        duration_days: int,
        cancel_date: datetime,
    ) -> float:
        """
        Розраховує суму повернення коштів за підписку.

        :param subscription_date: Дата початку підписки у форматі "YYYY-MM-DD"
        :param price: Повна вартість підписки
        :param duration_days: Тривалість підписки в днях
        :param cancel_date: Дата скасування у форматі "YYYY-MM-DD"
        :return: Сума для повернення
        """

        days_used = (cancel_date - sub_start_date).days

        if days_used <= 14:
            return price

        if days_used >= duration_days:
            return 0.0

        refund_amount = price * (1 - days_used / duration_days)
        return round(refund_amount, 2)

    async def cancel_preview_subscription(self, session: AsyncSession, user_id: int):
        logger.info("Launch the method to cancel preview subscription")

        subscription = await self.get_subscription(session, user_id)
        logger.info(f"subscription: {subscription}")

        if not subscription:
            return {
                "has_subscription": False,
                "refund_amount": 0.0,
                "full_refund": False,
            }
        cancel_date = datetime.now().date()
        refund_amount = self.calculate_refund_money(
            subscription.start_date.date(),
            subscription.plan.price,
            subscription.plan.duration_days,
            cancel_date,
        )
        full_refund = refund_amount == subscription.plan.price
        return {
            "has_subscription": True,
            "refund_amount": refund_amount,
            "full_refund": full_refund,
        }

    async def get_subscription(
        self, session: AsyncSession, user_id: int
    ) -> Optional[Subscription]:
        key = f"user_subscription_{user_id}"
        cached_subscription = await self.cache.get(key)
        if cached_subscription:
            return cached_subscription

        result = await self.crud_repository.read(
            select(Subscription).filter_by(master_id=user_id), session
        )
        subscription = result.scalar()
        ensure_resource_exists(subscription)
        await self.cache.set(key, subscription, ttl=18000)
        return subscription

    async def calculate_end_date(self, duration_days: int) -> datetime:
        return datetime.now() + timedelta(days=duration_days)

    async def activate_free_subscription(
        self,
        session: AsyncSession,
        user_id: int,
    ): ...

    async def create_subscription(
        self, session: AsyncSession, plan: SubscriptionPlan, user_id: int, chat_id: int
    ) -> Optional[Subscription]:
        logger.info("Створення підписки")
        end_date = await self.calculate_end_date(plan.duration_days)
        created_subscription = await self.crud_repository.create(
            Subscription(master_id=user_id, plan_id=plan.id, end_date=end_date),
            session,
        )

        if created_subscription:
            await self.cache.clear_cache(f"user_subscription_{user_id}")
            logger.info("Підписка створена успішно")
            await self.notification_service.send_message(
                chat_id, PAYMENT_MESSAGE["success_active_subscription"]
            )
        else:
            logger.error(
                f"Помилка при створенні підписки. Вхідні дані: user_id: {user_id} | plan_id: {plan.id}"
            )
            await self.notification_service.send_message(
                chat_id, PAYMENT_MESSAGE["error_activation_subscription"]
            )

        return created_subscription
