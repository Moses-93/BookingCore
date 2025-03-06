from sqlalchemy import (
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey,
    func,
)
from .base import Base


class BusinessInfo(Base):
    __tablename__ = "business_info"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(60), nullable=False)
    phone_number = Column(String(13), nullable=False)
    description = Column(String, nullable=True)
    working_hours = Column(String, nullable=False)
    google_maps_link = Column(String, nullable=True)
    telegram_link = Column(String, nullable=True)
    instagram_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    master_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    client_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    def __str__(self):
        return f"Назва: {self.name} | Адреса: {self.address} | Телефон: {self.phone_number}"
