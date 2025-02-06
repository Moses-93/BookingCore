from typing import Optional, List
from pydantic import BaseModel, Field
from .master import MasterResponse


class UserBase(BaseModel):
    name: str
    username: str
    phone: str
    chat_id: int = Field(..., ge=2)
    role: Optional[str]


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    role: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
