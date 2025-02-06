from pydantic import BaseModel, Field
from datetime import datetime


class MasterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class MasterCreate(MasterBase):
    pass


class MasterResponse(MasterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
