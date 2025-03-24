import logging

from typing import Any, Type

from sqlalchemy import Delete, Select, Update, and_, delete, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.declarative import DeclarativeMeta

from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces import BaseCRUD


logger = logging.getLogger(__name__)


class ImplementationCRUD(BaseCRUD):

    async def create(
        self,
        model: Type[DeclarativeMeta],
        session: AsyncSession,
        **kwargs: dict,
    ):
        logger.info(f"Запис даних в модель {model.__name__}, аргументи: {kwargs}")

        new_item = model(**kwargs)
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
        return new_item

    async def read(
        self,
        model: Type[DeclarativeMeta],
        session: AsyncSession,
        relations: tuple = None,
        expressions: tuple = None,
        limit: int = None,
        offset: int = 0,
        **filters,
    ):
        logger.info(f"Читання даних з моделі {model.__name__}, фільтри: {filters}")

        query = select(model)

        if relations:
            query = query.options(*[selectinload(rel) for rel in relations])

        if expressions is not None:
            query = query.filter(and_(*expressions))

        if filters:
            query = query.filter_by(**filters)

        # Застосовуємо пагінацію
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        try:
            result = await session.execute(query)
        except Exception as e:
            logger.error(f"Помилка під час читання з моделі {model.__name__}: {e}")
            return []

        return result

    async def update(
        self,
        model: Type[DeclarativeMeta],
        session: AsyncSession,
        expressions: tuple,
        **kwargs,
    ):
        logger.info(f"Оновлення даних в моделі: {model.__name__}, аргументи: {kwargs}")
        stmt = update(model).where(*expressions).values(**kwargs)
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

        except Exception as e:
            logger.error(f"Помилка під час оновлення з моделі {model.__name__}: {e}")

    async def delete(
        self,
        model: Type[DeclarativeMeta],
        session: AsyncSession,
        **kwargs,
    ):
        logger.info(f"Видалення даних з моделі: {model.__name__}, аргументи: {kwargs}.")
        stmt = delete(model).filter_by(**kwargs)
        try:
            result = await session.execute(stmt)
            await session.commit()
            if result.rowcount == 0:
                logger.warning(
                    f"Жодного рядка не було видалено з моделі {model.__name__}."
                )
                return False
        except Exception as e:
            logger.error(f"Помилка під час видалення з моделі {model.__name__}: {e}")
            return False
        return True


class CRUDRepository(BaseCRUD):

    async def create(
        self,
        query: Any,
        session: AsyncSession,
    ):
        session.add(query)
        await session.commit()
        await session.refresh(query)
        return query

    async def read(
        self,
        query: Select,
        session: AsyncSession,
    ):
        result = await session.execute(query)
        return result

    async def update(
        self,
        query: Update,
        session: AsyncSession,
    ) -> bool:
        result = await session.execute(query)
        await session.commit()
        return result.rowcount > 0

    async def delete(self, query: Delete, session: AsyncSession):
        result = await session.execute(query)
        await session.commit()
        return result.rowcount > 0
