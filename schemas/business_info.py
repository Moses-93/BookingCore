from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, model_validator


class BusinessInfoBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    address: str = Field(..., min_length=10, max_length=60)


class BusinessInfoCreate(BusinessInfoBase):
    phone: str = Field(..., min_length=13, max_length=13, pattern=r"^\+380\d{9}$")
    working_hours: str = Field(..., example="9:00-18:00", min_length=10, max_length=12)
    google_maps_url: Optional[HttpUrl] = Field(None, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=200)


class BusinessInfoUpdate(BusinessInfoBase):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    address: Optional[str] = Field(None, min_length=10, max_length=60)
    phone: Optional[str] = Field(
        None, min_length=13, max_length=13, pattern=r"^\+380\d{9}$"
    )
    working_hours: Optional[str] = Field(
        None, example="9:00-18:00", min_length=10, max_length=12
    )
    google_maps_url: Optional[HttpUrl] = Field(None, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=200)

    @model_validator(mode="before")
    def validate_data(cls, values):
        if not any(values.values()):
            raise ValueError("No fields provided for update")
        return values


class BusinessInfoResponse(BusinessInfoBase):
    id: int
    phone: str
    working_hours: str
    google_maps_url: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
