import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from core.dependencies import get_db, verify_user
from decorators.permissions import requires_role
from schemas import business_info
from db.models.business import BusinessInfo
from db.models.user import User
from db.crud import crud
from utils.validators import ensure_resource_exists


router = APIRouter(prefix="/business-info", tags=["business-info"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[business_info.BusinessInfoResponse])
@requires_role(["admin", "user"])
async def get_business_info(
    user: User = Depends(verify_user), db: AsyncSession = Depends(get_db)
):
    result = await crud.read(model=BusinessInfo, session=db)
    ensure_resource_exists(result)
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["admin"])
async def create_business_info(
    business_info: business_info.BusinessInfoCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    master = user.masters[0]
    logger.info(f"Business info: {business_info}")
    result = await crud.create(
        model=BusinessInfo,
        session=db,
        name=business_info.name,
        address=business_info.address,
        phone=business_info.phone,
        working_hours=business_info.working_hours,
        google_maps_link=business_info.google_maps_link,
        description=business_info.description,
        telegram_link=business_info.telegram_link,
        instagram_link=business_info.instagram_link,
        master_id=master.id
    )
    ensure_resource_exists(
        result, status_code=400, message="Failed to create business info"
    )
    return result


@router.patch("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["admin"])
async def update_business_info(
    name: str,
    business_info: business_info.BusinessInfoUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    master = user.masters[0]
    logger.info(f"Update business info:{name}")
    update_data = business_info.model_dump(exclude_unset=True)

    result = await crud.update(
        model=BusinessInfo,
        session=db,
        expressions=(BusinessInfo.master_id == master.id,),
        **update_data,
    )

    ensure_resource_exists(result)
