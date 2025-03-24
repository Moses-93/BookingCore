from typing import AsyncGenerator
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.core.config import settings

engine = create_async_engine(url=settings.database_url())
Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session


async def close_db():
    await engine.dispose()


def register_db_shutdown_event(app: FastAPI):
    app.add_event_handler("shutdown", close_db)
