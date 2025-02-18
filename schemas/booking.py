from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date, time

import schemas as schemas
import schemas.date
import schemas.service
import schemas.time
import schemas.user


class BookingBase(BaseModel):
    is_active: Optional[bool] = Field(default=True)


class BookingCreate(BookingBase):
    time_id: int
    service_id: int
    date_id: int
    master_id: Optional[int] = None
    reminder_time: Optional[datetime] = None
    date: date
    time: time
    service: str


class BookingUpdate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    user: schemas.user.UserResponse
    service: schemas.service.ServiceResponse
    date: schemas.date.DateResponse
    time: schemas.time.TimeResponse
    created_at: datetime

    class Config:
        from_attributes = True
