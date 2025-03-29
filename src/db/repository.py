import logging
from typing import List, Optional, Union
from sqlalchemy import Delete, Select, Update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces import BaseCRUD

logger = logging.getLogger(__name__)


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
