from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str
    username: Optional[str] = None
    chat_id: int = Field(..., ge=2)
    admin: Optional[bool] = Field(default=False)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
