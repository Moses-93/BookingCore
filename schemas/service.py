from datetime import timedelta
from pydantic import BaseModel, Field
from typing import Optional


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: int = Field(..., ge=0)
    duration: timedelta


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    name: Optional[str] = Field(..., min_length=2, max_length=50)
    price: Optional[int] = Field(..., ge=0)
    duration: Optional[timedelta]


class ServiceResponse(ServiceBase):
    id: int

    class Config:
        orm_mode = True
