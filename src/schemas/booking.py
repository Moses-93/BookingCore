from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date, time

from src.schemas.date import DateResponse
from src.schemas.service import ServiceResponse
from src.schemas.time import TimeResponse
from src.schemas.user import UserResponse


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
    user: UserResponse
    service: ServiceResponse
    date: DateResponse
    time: TimeResponse
    created_at: datetime

    class Config:
        from_attributes = True
