import logging
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from .subscription import SubscriptionResponse
from utils.encryption import encryption_service


logger = logging.getLogger(__name__)


class UserBase(BaseModel):
    name: str
    username: str
    phone_number: str
    chat_id: int = Field(..., ge=2)
    role: Optional[str]
    is_active: Optional[bool] = Field(default=True)


class UserCreate(UserBase):
    master_chat_id: Optional[int]

    @field_validator("phone_number", mode="before")
    @classmethod
    def enctypy_phone(csl, value: str) -> str:
        logger.info(f"Запуск методу для кодування номеру телефона")
        if not isinstance(value, str):
            logger.warning(f"Номер телефону не є рядком: {value}")
        return encryption_service.encrypt(value)


class UserUpdate(UserBase):
    role: Optional[str] = None


class MasterResponse(BaseModel):
    name: str
    username: Optional[str] = None
    chat_id: int


class MasterLinkRequest(BaseModel):
    master_chat_id: int


class UserResponse(UserBase):
    id: int
    masters: List[MasterResponse] = []

    class Config:
        from_attributes = True

    @field_validator("phone_number")
    @classmethod
    def decrypt_phone(cls, value: str) -> str:
        logger.info(f"Запуск методу для декодування номеру телефона")
        if not isinstance(value, str):
            logger.warning(f"Номер телефону не є рядком: {value}")
            raise ValueError("Phone number must be a string")
        return encryption_service.decrypt(value)
