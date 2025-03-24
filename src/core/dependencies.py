import logging
from fastapi import Depends, HTTPException, Request, status
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from db.models import user as u
from core.config import settings

from core.dependency_factory import DependencyFactory
from api.v1.handler_factory import HandlerFactory
from api.v1.api_factory import APIFactory


logger = logging.getLogger(__name__)
engine = create_async_engine(url=settings.database_url())
Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

dependency_factory = DependencyFactory()
handler_factory = HandlerFactory(dependency_factory)
api_factory = APIFactory(handler_factory)

def get_dependency_factory():
    return dependency_factory

def get_handler_factory():
    return handler_factory

def get_api_factory():
    return api_factory

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session


async def verify_user(request: Request, db: AsyncSession = Depends(get_db)):
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
    result = await dependency_factory.crud_repository.read(
        u.User, db, chat_id=telegram_chat_id, relations=(u.User.masters,)
    )
    user = result.scalar()

    if user is None:
        logger.warning(f"Користувач з ID: {telegram_chat_id} не знайдений")
        return None

    logger.info(f"Користувач з ID: {telegram_chat_id} пройшов автентифікацію")
    return user


async def get_current_user(request: Request) -> Optional[u.User]:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
