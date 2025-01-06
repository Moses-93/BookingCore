from typing import Optional
from pydantic import BaseModel, Field

from datetime import date


class DateBase(BaseModel):
    date: date
    free: Optional[bool] = Field(default=True)


class DateCreate(DateBase):
    pass


class DateResponse(DateBase):
    id: int

    class Config:
        orm_mode = True
