from typing import Optional
from pydantic import BaseModel, Field
from datetime import time


class TimeBase(BaseModel):
    time: time


class TimeCreate(TimeBase):
    active: Optional[bool] = Field(default=True)
    date_id: int


class TimeResponse(TimeBase):
    id: int

    class Config:
        from_attributes = True
