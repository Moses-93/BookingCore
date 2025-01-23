from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str
    chat_id: int = Field(..., ge=2)


class UserCreate(UserBase):
    role: Optional[str]


class UserUpdate(UserBase):
    name: Optional[str] = None
    role: Optional[str] = None
    username: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
