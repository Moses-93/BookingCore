# from asgiref.sync import async_to_sync
# from datetime import datetime, timedelta
# from sqlalchemy import and_, select
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
# from core.dependencies import get_db
# from db.models.subscription import Subscription
# from db.crud import new_crud
# from services.notifications import send_message
# from ..celery_app import celery_app
# import logging

# logger = logging.getLogger(__name__)


# @celery_app.task(name="check_subscriptions")
# def check_subscriptions():
#     async_to_sync(_check_subscriptions)()


# async def _check_subscriptions():
#     now = datetime.now()
#     five_days_later = now + timedelta(days=5)
#     one_day_later = now + timedelta(days=1)

#     try:
#         session: AsyncSession = await anext(get_db())

#         # Запит для підписок, які закінчуються через 5 днів
#         query_five_days = (
#             select(Subscription)
#             .options(selectinload(Subscription.user))
#             .filter(
#                 and_(
#                     Subscription.end_date >= five_days_later,
#                     Subscription.end_date < five_days_later + timedelta(days=1),
#                 )
#             )
#         )

#         # Запит для підписок, які закінчуються через 1 день
#         query_one_day = (
#             select(Subscription)
#             .options(selectinload(Subscription.user))
#             .filter(
#                 and_(
#                     Subscription.end_date >= one_day_later,
#                     Subscription.end_date < one_day_later + timedelta(days=1),
#                 )
#             )
#         )

#         # Отримуємо підписки
#         subscriptions_five_days = await new_crud.read(query_five_days, session)
#         subscriptions_one_day = await new_crud.read(query_one_day, session)

#         # Відправляємо нагадування
#         for subscription in subscriptions_five_days:
#             try:
#                 send_message(
#                     subscription.user.chat_id,
#                     "Ваша підписка закінчується через 5 днів.",
#                 )
#                 logger.info(
#                     f"Нагадування відправлено користувачу {subscription.user.id}."
#                 )
#             except Exception as e:
#                 logger.error(f"Помилка під час відправки повідомлення: {e}")

#         for subscription in subscriptions_one_day:
#             try:
#                 send_message(
#                     subscription.user.chat_id, "Ваша підписка закінчується завтра."
#                 )
#                 logger.info(
#                     f"Нагадування відправлено користувачу {subscription.user.id}."
#                 )
#             except Exception as e:
#                 logger.error(f"Помилка під час відправки повідомлення: {e}")

#     except Exception as e:
#         logger.error(f"Помилка під час виконання задачі: {e}")
#     finally:
#         await session.close()
