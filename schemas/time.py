from typing import Optional
from pydantic import BaseModel, Field
from datetime import time, date


class TimeBase(BaseModel):
    time: time
    is_active: Optional[bool] = Field(default=True)
    date_id: int


class TimeCreate(TimeBase):
    date: date


class TimeResponse(TimeBase):
    id: int

    class Config:
        from_attributes = True
