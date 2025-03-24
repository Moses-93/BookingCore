import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_db, get_current_user
from decorators.permissions import requires_role
from schemas.user import UserCreate, UserResponse, MasterLinkRequest
from db.models.user import User
from services.user.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
@requires_role(["admin", "master", "client"])
async def get_user(user: User = Depends(get_current_user)):
    logger.info(f"User: {user}")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    new_user = await UserService(db).create_user(user_data)
    return new_user


@router.post("/masters/", status_code=status.HTTP_204_NO_CONTENT)
async def link_master_to_user(
    master: MasterLinkRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await UserService(db).add_master_to_user(user.id, master.master_chat_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["client", "master"])
async def delete_user(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await UserService(db).delete_user(user.id)
