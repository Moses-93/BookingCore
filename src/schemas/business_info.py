from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, model_validator


class BusinessInfoBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    address: str = Field(..., min_length=10, max_length=60)
    phone_number: str = Field(
        ..., min_length=13, max_length=13, pattern=r"^\+380\d{9}$"
    )


class BusinessInfoCreate(BusinessInfoBase):
    google_maps_link: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=200)
    telegram_link: Optional[str] = None
    instagram_link: Optional[str] = None


class BusinessInfoUpdate(BusinessInfoBase):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    address: Optional[str] = Field(None, min_length=10, max_length=60)
    phone_number: Optional[str] = Field(
        None, min_length=13, max_length=13, pattern=r"^\+380\d{9}$"
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
    phone_number: str
    google_maps_link: Optional[str]
    telegram_link: Optional[str]
    instagram_link: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
