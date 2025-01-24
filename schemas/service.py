from datetime import timedelta
from pydantic import BaseModel, Field, model_validator
from typing import Optional


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: int = Field(..., ge=0)
    duration: timedelta


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    price: Optional[int] = Field(None, ge=0)
    duration: Optional[timedelta]

    @model_validator(mode="before")
    def validate_data(cls, values):
        if not any(values.values()):
            raise ValueError("No fields provided for update")
        return values


class ServiceResponse(ServiceBase):
    id: int

    class Config:
        from_attributes = True
