import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from typing import List, Optional, Union

from src.db.models.user import User
from src.schemas.business_info import BusinessInfoCreate, BusinessInfoUpdate
from src.db.models.business import BusinessInfo
from src.db.repository import CRUDRepository
from src.utils import RedisCacheFactory


logger = logging.getLogger(__name__)


class BusinessInfoService:

    def __init__(
        self, crud_repository: CRUDRepository, cache_factory: RedisCacheFactory
    ):
        self.crud_repository = crud_repository
        self.cache = cache_factory

    async def create_business_info(
        self,
        session: AsyncSession,
        business_info_data: BusinessInfoCreate,
        user_id: int,
    ) -> Optional[BusinessInfo]:
        await self.cache.get_cache().client.rpu(f"business-info-master-id={user_id}")
        logger.info(f"Business info: {business_info_data}")
        business_info_dump = business_info_data.model_dump()
        business_info_dump["master_id"] = user_id
        logger.info(f"business_info_dump: {business_info_dump}")
        stmt = BusinessInfo(**business_info_dump)
        created_business_info = await self.crud_repository.create(stmt, session)
        return created_business_info

    async def get_business_info(
        self, session: AsyncSession, user: User, master_id: Union[int, None]
    ) -> Optional[List[BusinessInfo]]:
        filters = {}
        if not master_id:
            filters = await self.user_tools.identify_role(user, filters)
        logger.info(f"filters: {filters}")
        result = await self.crud_repository.read(
            select(BusinessInfo).filter_by(**filters), session
        )
        business_info = result.scalars().all()

        return business_info

    async def update_business_info(
        self,
        session: AsyncSession,
        user_id: int,
        updating_business_info: BusinessInfoUpdate,
    ) -> bool:
        update_data = updating_business_info.model_dump(exclude_unset=True)

        return await self.crud_repository.update(
            update(BusinessInfo)
            .where(BusinessInfo.master_id == user_id)
            .values(**update_data),
            session,
        )
