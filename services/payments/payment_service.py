import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select

from core.constants import PAYMENT_MESSAGE

from db.models import payment as p, user as u
from db.crud import new_crud

from ..notifications import notification_service, NotificationService
from ..subscription import subscription_service, SubscriptionService

logger = logging.getLogger(__name__)


class PaymentService:

    def __init__(
        self,
        subscription_manager: SubscriptionService,
        notification_manager: NotificationService,
    ):
        self.subscription_manager = subscription_manager
        self.notification_manager = notification_manager

    async def get_payment(
        self, session: AsyncSession, order_id: str
    ) -> Optional[p.Payment]:
        """Отримує платіж за order_id."""
        result = await new_crud.read(
            select(p.Payment).filter_by(order_id=order_id), session
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
        payment = p.Payment(
            subscription_plan_id=subscription_plan_id,
            user_id=user_id,
            order_id=order_id,
            amount=amount,
        )
        await new_crud.create(payment, session)

    async def update_payment_status(
        self,
        session: AsyncSession,
        order_id: str,
        payment_method: str,
        transaction_status: str,
    ) -> None:
        """Оновлює статус платежу."""
        await new_crud.update(
            update(p.Payment)
            .where(p.Payment.order_id == order_id)
            .values(payment_method=payment_method, status=transaction_status),
            session,
        )

    async def handle_successful_payment(
        self, session: AsyncSession, payment: p.Payment
    ) -> None:
        """Обробляє успішний платіж."""
        user = await session.get(u.User, payment.user_id)
        await self.notification_manager.send_message(
            user.chat_id, PAYMENT_MESSAGE["received_payment"]
        )
        await self.subscription_manager.create_subscription(
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


payment_service = PaymentService(subscription_service, notification_service)
