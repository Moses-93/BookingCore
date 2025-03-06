import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from typing import List

from schemas import business_info
from db.models.business import BusinessInfo
from db.crud import new_crud

logger = logging.getLogger(__name__)

class BusinessInfoService:

    async def create_business_info(self, session: AsyncSession, business_info_data: business_info.BusinessInfoCreate, user_id: int):
        logger.info(f"Business info: {business_info}")
        business_info_dump = business_info_data.model_copy(update={"master_id": user_id}).model_dump()
        query = BusinessInfo(**business_info_dump)
        created_business_info = await new_crud.create(query, session)
        return created_business_info
    

business_info_service = BusinessInfoService()