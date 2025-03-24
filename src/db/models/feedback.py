from sqlalchemy import (
    Text,
    Integer,
    Column,
    DateTime,
    ForeignKey,
    func,
)
from .base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    master_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

    def __str__(self):
        return f"Ім'я: {self.user.name} | Рейтинг: {self.rating} | Коментар: {self.comment}"
