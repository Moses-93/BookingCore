from pydantic import BaseModel, Field

from datetime import date, datetime


class DateBase(BaseModel):
    date: date
    is_active: bool = Field(default=True)


class DateCreate(DateBase):
    deactivation_time: datetime


class DateResponse(DateBase):
    id: int

    class Config:
        from_attributes = True
