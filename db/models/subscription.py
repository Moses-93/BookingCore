from sqlalchemy.orm import relationship
from sqlalchemy import (
    String,
    Integer,
    Float,
    Column,
    DateTime,
    ForeignKey,
    func,
)
from .base import Base


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    duration_days = Column(Integer, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    subscriptions = relationship("Subscription", back_populates="plan")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    master_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    plan_id = Column(
        Integer, ForeignKey("subscription_plans.id", ondelete="CASCADE"), nullable=False
    )
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    plan = relationship(
        "SubscriptionPlan", back_populates="subscriptions", lazy="joined"
    )
