import logging
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from utils.encryption import encription_service


logger = logging.getLogger(__name__)


class UserBase(BaseModel):
    name: str
    username: str
    phone: str
    chat_id: int = Field(..., ge=2)
    role: Optional[str]
    is_active: Optional[bool] = Field(default=True)


class UserCreate(UserBase):
    master_id: Optional[int]

    @field_validator("phone", mode="before")
    @classmethod
    def enctypy_phone(csl, value: str) -> str:
        logger.info(f"Запуск методу для кодування номеру телефона")
        if not isinstance(value, str):
            logger.warning(f"Номер телефону не є рядком: {value}")
        return encription_service.encrypt(value)


class UserUpdate(UserBase):
    role: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator("phone")
    @classmethod
    def decrypt_phone(cls, value: str) -> str:
        logger.info(f"Запуск методу для декодування номеру телефона")
        if not isinstance(value, str):
            logger.warning(f"Номер телефону не є рядком: {value}")
            raise ValueError("Phone number must be a string")
        return encription_service.decrypt(value)
