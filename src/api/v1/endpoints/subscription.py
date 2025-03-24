import logging
from typing import Dict, Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_db, get_current_user
from db.models.user import User
from decorators.permissions import requires_role
from services.subscription import subscription_plan_service, subscription_service
from schemas import subscription as s

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("/plans/", status_code=status.HTTP_200_OK)
@requires_role(["master"])
async def get_subscription_plans(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await subscription_plan_service.get_plans(db)


@router.get("/plans/{plan_id}", status_code=status.HTTP_200_OK)
@requires_role(["master"])
async def get_subscription_plan(
    plan_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await subscription_plan_service.get_plan(db, plan_id)


@router.get("/", status_code=status.HTTP_200_OK)
@requires_role(["master"])
async def get_subscription(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await subscription_service.get_subscription(db, user.id)


@router.post("/activate-free-plan", status_code=status.HTTP_201_CREATED)
@requires_role(["master"])
async def create_subscription(
    plan: s.SubscriptionActivate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    logger.info(f"plan:{plan}")

    await subscription_service.create_subscription(db, user.id, plan.id)


@router.get(
    "/cancel-preview",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Union[float, bool]],
)
@requires_role(["master"])
async def cancel_preview_subscription(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Launch the handler to cancel preview subscription")
    return await subscription_service.cancel_preview_subscription(db, user.id)
