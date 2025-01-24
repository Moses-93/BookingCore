import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from core.dependencies import get_db, verify_user
from decorators.permissions import requires_role
from schemas.user import UserCreate, UserResponse
from db.models import User
from db.crud import crud
from utils.validators import ensure_resource_exists


router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
@requires_role(["admin"])
async def get_user(
    user: User = Depends(verify_user), db: AsyncSession = Depends(get_db)
):
    users = await crud.read(model=User, session=db)
    ensure_resource_exists(users)
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
@requires_role(["admin"])
async def create_user(
    users: UserCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_user),
):
    exist_fields = users.model_dump(exclude_unset=True)
    data = await crud.create(
        model=User,
        session=db,
        **exist_fields,
    )
    ensure_resource_exists(
        data, status_code=400, message="Invalid data for user creation"
    )
    return data


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["admin"])
async def delete_user(
    user_id: int,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
):
    if user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users cannot delete themselves",
        )

    result = await crud.delete(
        model=User,
        session=db,
        id=user_id,
    )
    ensure_resource_exists(result)
