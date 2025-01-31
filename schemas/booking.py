from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, time

import schemas as schemas
import schemas.date
import schemas.service
import schemas.user


class BookingBase(BaseModel):
    active: Optional[bool] = Field(default=True)
    time: time


class BookingCreate(BookingBase):
    time: str
    service_id: int
    date_id: int
    master_id: Optional[int] = None


class BookingUpdate(BookingBase):
    reminder_hours: Optional[int] = Field(None, ge=0)


class BookingResponse(BookingBase):
    id: int
    name: schemas.user.UserResponse
    service: schemas.service.ServiceResponse
    date: schemas.date.DateResponse
    created_at: datetime

    class Config:
        from_attributes = True
