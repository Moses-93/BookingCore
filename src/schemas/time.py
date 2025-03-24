from typing import Optional
from pydantic import BaseModel, Field
from datetime import time, date
from .date import DateResponse


class TimeBase(BaseModel):
    time: time
    is_active: Optional[bool] = Field(default=True)
    date_id: int


class TimeCreate(TimeBase):
    date: date


class TimeResponse(TimeBase):
    id: int
    date: DateResponse

    class Config:
        from_attributes = True
