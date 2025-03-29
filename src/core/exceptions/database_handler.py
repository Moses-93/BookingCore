import logging
from functools import wraps
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    ProgrammingError,
    InvalidRequestError,
)
from .database_exc import (
    DBIntegrityError,
    DBCreateError,
    DBReadError,
    DBUpdateError,
    DBDeleteError,
)

logger = logging.getLogger(__name__)

exceptions = {
    "create": DBCreateError,
    "read": DBReadError,
    "update": DBUpdateError,
    "delete": DBDeleteError,
}


def handle_db_exceptions(operation: str):
    """Decorator for handling database errors in CRUD methods."""

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except IntegrityError as e:
                await args[1].rollback()
                logger.error(f"Integrity error during {operation}: {e}", exc_info=True)
                raise DBIntegrityError(f"Integrity error during {operation}: {e}")
            except (OperationalError, ProgrammingError, InvalidRequestError) as e:
                await args[1].rollback()
                logger.error(f"Database error during {operation}: {e}", exc_info=True)
                raise exceptions[operation](f"Database error during {operation}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during {operation}: {e}", exc_info=True)
                raise

        return wrapper

    return decorator
