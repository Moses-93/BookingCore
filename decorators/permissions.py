import logging
from fastapi import HTTPException
from functools import wraps
from db.models import User


logger = logging.getLogger(__name__)


def requires_role(roles: list[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info("Авторизація користувача")
            user: User = kwargs.get("user")
            if not user:
                logger.warning("Користувач не знайдений")
                raise HTTPException(status_code=401, detail="User not found")
            if user.role not in roles:
                logger.warning(f"Користувач з ролью {user.role} не має необхідних прав")
                raise HTTPException(
                    status_code=403, detail="Forbidden: Insufficient permissions"
                )
            logger.info(
                f"Користувач: {user.chat_id} з ролью {user.role} успішно авторизований"
            )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
