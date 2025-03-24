import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select

from src.core.constants import PAYMENT_MESSAGE
from src.db.models import User, Payment
from src.db.repository import CRUDRepository
from src.services.notifications import NotificationService
from src.services.subscription import SubscriptionService

logger = logging.getLogger(__name__)


class PaymentService:

    def __init__(
        self,
        crud_repository: CRUDRepository,
        subscription_service: SubscriptionService,
        notification_service: NotificationService,
    ):
        self.crud_repository = crud_repository
        self.subscription_service = subscription_service
        self.notification_service = notification_service

    async def get_payment(
        self, session: AsyncSession, order_id: str
    ) -> Optional[Payment]:
        """Отримує платіж за order_id."""
        result = await self.crud_repository.read(
            select(Payment).filter_by(order_id=order_id), session
        )
        return result.scalar()

    async def create_payment(
        self,
        session: AsyncSession,
        subscription_plan_id: int,
        user_id: int,
        order_id: str,
        amount: int,
    ) -> None:
        """Створює новий платіж."""
        payment = Payment(
            subscription_plan_id=subscription_plan_id,
            user_id=user_id,
            order_id=order_id,
            amount=amount,
        )
        await self.crud_repository.create(payment, session)

    async def update_payment_status(
        self,
        session: AsyncSession,
        order_id: str,
        payment_method: str,
        transaction_status: str,
    ) -> None:
        """Оновлює статус платежу."""
        await self.crud_repository.update(
            update(Payment)
            .where(Payment.order_id == order_id)
            .values(payment_method=payment_method, status=transaction_status),
            session,
        )

    async def handle_successful_payment(
        self, session: AsyncSession, payment: Payment
    ) -> None:
        """Обробляє успішний платіж."""
        user = await session.get(User, payment.user_id)
        await self.notification_manager.send_message(
            user.chat_id, PAYMENT_MESSAGE["received_payment"]
        )
        await self.subscription_service.create_subscription(
            session, payment.user_id, payment.subscription_plan_id, user.chat_id
        )

    async def process_payment(
        self,
        session: AsyncSession,
        order_id: str,
        payment_method: str,
        transaction_status: str,
    ) -> None:
        """Обробляє платіж (оновлює статус та нараховує підписку, якщо потрібно)."""
        await self.update_payment_status(
            session, order_id, payment_method, transaction_status
        )

        if transaction_status == "Approved":
            payment = await self.get_payment(session, order_id)
            if payment:
                await self.handle_successful_payment(session, payment)
            else:
                logger.error(f"Платіж з order_id {order_id} не знайдено.")
        else:
            logger.warning(
                f"Статус платежу: {transaction_status}! Платіж не підтверджено. Підписку не нараховано."
            )
