from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SubscriptionPlanBase(BaseModel):
    name: str
    price: int


class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass


class SubscriptionPlanUpdate(SubscriptionPlanBase):
    name: Optional[str] = None
    price: Optional[int] = None


class SubscriptionPlanResponse(SubscriptionPlanBase):
    id: int

    class Config:
        from_attributes = True


class SubscriptionBase(BaseModel):
    id: int


class SubscriptionActivate(SubscriptionBase):
    pass


class SubscriptionUpdate(SubscriptionBase):
    plan_id: Optional[int] = None


class SubscriptionResponse(SubscriptionBase):
    id: int
    plan: SubscriptionPlanResponse
    start_date: datetime
    end_date: datetime
