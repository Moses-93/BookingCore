from typing import Optional, List
from pydantic import BaseModel, Field
from .master import MasterResponse


class UserBase(BaseModel):
    name: str
    username: str
    phone: str
    chat_id: int = Field(..., ge=2)
    role: Optional[str]
    master_id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = None
    role: Optional[str] = None
    username: Optional[str] = None


class UserResponse(UserBase):
    id: int
    masters: List[MasterResponse]

    class Config:
        from_attributes = True
