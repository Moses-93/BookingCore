import logging
from typing import List, Optional, Union
from sqlalchemy import Delete, Select, Update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions.database_handler import handle_db_exceptions

from .interfaces import BaseCRUD

logger = logging.getLogger(__name__)


class CRUDRepository(BaseCRUD):

    @staticmethod
    @handle_db_exceptions("create")
    async def create(query: DeclarativeBase, session: AsyncSession) -> DeclarativeBase:
        """Creates a new entry in the database.

        Args:
            query (DeclarativeBase): An instance of a SQLAlchemy model
            session (AsyncSession): Asynchronous session to perform the operation

        Returns:
            DeclarativeBase: Created model object
        """
        session.add(query)
        await session.commit()
        await session.refresh(query)
        return query

    @staticmethod
    @handle_db_exceptions("read")
    async def read(
        query: Select, session: AsyncSession, single: bool = False
    ) -> Union[Optional[DeclarativeBase], List[DeclarativeBase]]:
        """Executes a SELECT query to the database

        Args:
            query (Select): SQLAlchemy Select-query
            session (AsyncSession): Asynchronous session to perform the operation
            single (bool, optional):  if True, returns a single object (or None), otherwise - a list. Defaults to False.

        Returns:
            Union[Optional[DeclarativeBase], List[DeclarativeBase]]: One model object (single=True) or List of objects (single=False).
        """
        result = await session.execute(query)
        return result.scalars().first() if single else result.scalars().all()

    @staticmethod
    @handle_db_exceptions("update")
    async def update(query: Update, session: AsyncSession) -> bool:
        """Executes a UPDATE query to the database

        Args:
            query (Update): SQLAlchemy Update-query
            session (AsyncSession): Asynchronous session to perform the operation

        Returns:
            bool: A Boolean value indicating whether changes have occurred in the database
        """
        result = await session.execute(query)
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    @handle_db_exceptions("delete")
    async def delete(query: Delete, session: AsyncSession) -> bool:
        """Executes a UPDATE query to the database

        Args:
            query (Delete): SQLAlchemy Delete-query
            session (AsyncSession): Asynchronous session to perform the operation

        Returns:
            bool: A Boolean value indicating whether changes have occurred in the database
        """
        result = await session.execute(query)
        await session.commit()
        return result.rowcount > 0
