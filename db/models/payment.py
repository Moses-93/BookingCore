from sqlalchemy import (
    String,
    Integer,
    Enum,
    Column,
    DateTime,
    ForeignKey,
    func,
)
from .base import Base


class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    subscription_id = Column(
        Integer, ForeignKey("subscriptions.id"), nullable=False, index=True
    ) 
    order_id = Column(
        String, unique=True, nullable=False, index=True
    )
    transaction_id = Column(
        String, unique=True, nullable=True
    )
    amount = Column(Integer, nullable=False)
    payment_date = Column(DateTime, default=func.now())
    payment_method = Column(
        String, nullable=False
    )
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
