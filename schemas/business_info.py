from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field, HttpUrl


class BusinessInfoBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    address: str = Field(..., min_length=10, max_length=60)


class BusinessInfoCreate(BusinessInfoBase):
    phone: str = Field(..., min_length=13, max_length=13, regex=r"^\+380\d{9}$")
    working_hours: Dict[str, str] = Field(
        ..., example={"weekdays": "9:00-18:00", "weekends": "10:00-15:00"}
    )


class BusinessInfoUpdate(BusinessInfoBase):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    address: Optional[str] = Field(None, min_length=10, max_length=60)
    phone: Optional[str] = Field(None, min_length=13, max_length=13, regex=r"^\+?\d+$")
    working_hours: Optional[Dict[str, str]] = Field(
        None, example={"weekdays": "9:00-18:00"}
    )
    google_maps_url: Optional[HttpUrl] = Field(None, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=200)


class BusinessInfoResponse(BusinessInfoBase):
    id: int
    phone: str
    working_hours: Dict[str, str]
    google_maps_url: Optional[HttpUrl]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
