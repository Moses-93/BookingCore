from pydantic import BaseModel, Field
from datetime import datetime, timedelta, date, time
from typing import Optional


class DateBase(BaseModel):
    date: date
    free: Optional[bool] = Field(default=True)


class DateCreate(DateBase):
    pass


class DateResponse(DateBase):
    id: int

    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: int = Field(..., ge=0)
    duration: timedelta


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    name: str = Field(..., min_length=2, max_length=50)
    price: int = Field(..., ge=0)
    duration: timedelta

    class Config:
        orm_mode = True


class ServiceResponse(ServiceBase):
    id: int

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    active: Optional[bool] = Field(default=True)
    time: time
    reminder_hours: Optional[int] = Field(None, ge=0)


class BookingCreate(BookingBase):
    name_id: int
    service_id: int
    date_id: int


class BookingUpdate(BookingBase):
    active: Optional[bool] = Field(default=True)
    reminder_hours: Optional[int] = Field(None, ge=0)

    class Config:
        orm_mode = True


class BookingResponse(BookingBase):
    id: int
    name: str
    service: ServiceResponse
    date: DateResponse
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    username: Optional[str] = None
    chat_id: int = Field(..., ge=2)
    admin: Optional[bool] = Field(default=False)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: str
    username: Optional[str] = None
    admin: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
