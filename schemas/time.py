from typing import Optional
from pydantic import BaseModel, Field
from datetime import time


class TimeBase(BaseModel):
    time: time
    active: Optional[bool] = Field(default=True)


class TimeCreate(BaseModel):
    date_id:int


class TimeResponse(TimeBase):
    id: int

    class Config:
        from_attributes = True