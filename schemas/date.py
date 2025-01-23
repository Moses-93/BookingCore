from typing import Optional
from pydantic import BaseModel, Field

from datetime import date, datetime


class DateBase(BaseModel):
    date: date
    free: Optional[bool] = Field(default=True)


class DateCreate(DateBase):
    del_time: datetime


class DateResponse(DateBase):
    id: int

    class Config:
        from_attributes = True
