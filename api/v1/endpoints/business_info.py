import logging
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from core.dependencies import get_db, get_current_user
from decorators.permissions import requires_role
from schemas.business_info import (
    BusinessInfoResponse,
    BusinessInfoCreate,
    BusinessInfoUpdate,
)
from db.models.user import User
from utils.validators import ensure_resource_exists
from services.business_info_service import business_info_service


router = APIRouter(prefix="/business-info", tags=["business-info"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[BusinessInfoResponse])
@requires_role(["master", "client"])
async def get_business_info(
    master_id: int | None = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    business_info_data = await business_info_service.get_business_info(
        db, user, master_id
    )
    logger.info(f"business_info: {business_info_data}")

    return business_info_data


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["master"])
async def create_business_info(
    business_info: BusinessInfoCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    created_business_info = await business_info_service.create_business_info(
        db, business_info, user.id
    )
    ensure_resource_exists(
        created_business_info, status_code=422, message="Failed to create business info"
    )
    return created_business_info


@router.patch("/", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["master"])
async def update_business_info(
    business_info: BusinessInfoUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await business_info_service.update_business_info(
        db, user.id, business_info
    )

    ensure_resource_exists(result)
