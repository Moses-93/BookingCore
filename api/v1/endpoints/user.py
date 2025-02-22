import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from typing import List

from core.dependencies import get_db, verify_user
from decorators.permissions import requires_role
from schemas.user import UserCreate, UserResponse
from db.models import User, user_master_association
from db.crud import crud
from utils.validators import ensure_resource_exists

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
@requires_role(["admin"])
async def get_user(
    user: User = Depends(verify_user), db: AsyncSession = Depends(get_db)
):
    result = await crud.read(model=User, session=db)
    users = result.unique().scalars().all()
    ensure_resource_exists(users)
    return users


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user_data = user.model_dump(exclude={"master_id"})
    new_user = await crud.create(model=User, session=db, **user_data)
    logger.info(f"New user: {new_user}")
    ensure_resource_exists(
        new_user, status_code=400, message="Invalid data for user creation"
    )
    stmt = insert(user_master_association).values(
        user_id=new_user.id, master_id=user.master_id
    )
    await db.execute(stmt)
    await db.commit()
    logger.info(f"User {new_user.name} created successfully")

    return new_user


@router.post("/masters/", status_code=status.HTTP_204_NO_CONTENT)
async def link_master_to_user(
    master:MasterLinkRequest,
    user: User = Depends(verify_user),
    db: AsyncSession = Depends(get_db),
    ):
    await UserService(db).add_master_to_user(user.id, master.master_chat_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
@requires_role(["client", "master"])
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
