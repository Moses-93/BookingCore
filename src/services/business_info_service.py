import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from typing import List, Optional, Union

from db.models.user import User
from schemas.business_info import BusinessInfoCreate, BusinessInfoUpdate
from db.models.business import BusinessInfo
from db.crud import new_crud
from .user import user_tools, UserTools


logger = logging.getLogger(__name__)

class BusinessInfoService:

    def __init__(self, user_tools: UserTools):
        self.user_tools = user_tools

    async def create_business_info(
        self,
        session: AsyncSession,
        business_info_data: BusinessInfoCreate,
        user_id: int,
    ) -> Optional[BusinessInfo]:
        logger.info(f"Business info: {business_info_data}")
        business_info_dump = business_info_data.model_dump()
        business_info_dump["master_id"] = user_id
        logger.info(f"business_info_dump: {business_info_dump}")
        stmt = BusinessInfo(**business_info_dump)
        created_business_info = await new_crud.create(stmt, session)
        return created_business_info

    async def get_business_info(
        self, session: AsyncSession, user: User, master_id: Union[int, None]
    ) -> Optional[List[BusinessInfo]]:
        filters = {}
        if not master_id:
            filters = await self.user_tools.identify_role(user, filters)
        logger.info(f"filters: {filters}")
        result = await new_crud.read(select(BusinessInfo).filter_by(**filters), session)
        business_info = result.scalars().all()

        return business_info

    async def update_business_info(
        self,
        session: AsyncSession,
        user_id: int,
        updating_business_info: BusinessInfoUpdate,
    ) -> bool:
        update_data = updating_business_info.model_dump(exclude_unset=True)

        return await new_crud.update(
            update(BusinessInfo)
            .where(BusinessInfo.master_id == user_id)
            .values(**update_data),
            session,
        )


business_info_service = BusinessInfoService(user_tools)
