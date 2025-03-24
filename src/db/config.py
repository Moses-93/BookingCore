from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import settings

engine = create_async_engine(url=settings.database_url())
Session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
