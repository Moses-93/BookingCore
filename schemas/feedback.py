from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FeedbackBase(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
