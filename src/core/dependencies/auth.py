import logging
from fastapi import Depends, HTTPException, Request, status
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from .database import get_db
from .dependency_factory import DependencyFactory

logger = logging.getLogger(__name__)


async def verify_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    deps: DependencyFactory = Depends(lambda: DependencyFactory()),
):
    chat_id = request.headers.get("X-Chat-ID")
    if not chat_id:
        logger.warning("Не знайдено chat_id в заголовку запиту")
        return None

    try:
        telegram_chat_id = int(chat_id)
    except ValueError:
        logger.warning("Неправильний формат chat_id")
        return None

    logger.info(f"Автентифікація користувача з ID: {telegram_chat_id}")
    result = await deps.crud_repository.read(
        User, db, chat_id=telegram_chat_id, relations=(User.masters,)
    )
    user = result.scalar()

    if user is None:
        logger.warning(f"Користувач з ID: {telegram_chat_id} не знайдений")
        return None

    logger.info(f"Користувач з ID: {telegram_chat_id} пройшов автентифікацію")
    return user


async def get_current_user(request: Request) -> Optional[User]:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
