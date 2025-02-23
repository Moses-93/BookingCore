from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean,
    Time,
    Integer,
    Column,
    DateTime,
    ForeignKey,
    Date,
    func,
)

from .base import Base


class Date(Base):
    __tablename__ = "dates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    deactivation_time = Column(DateTime, nullable=False)
    master_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime, default=func.now())

    bookings = relationship("Booking", back_populates="date", lazy="joined")

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class Time(Base):
    __tablename__ = "times"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean, default=True, index=True)
    time = Column(Time, nullable=False)
    date_id = Column(
        Integer, ForeignKey("dates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at = Column(DateTime, default=func.now())

    date = relationship("Date", uselist=False, backref="time", lazy="joined")
    bookings = relationship("Booking", back_populates="time")

    def __str__(self):
        return f"Час: {self.time}"


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True, index=True)
    reminder_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    time_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    date_id = Column(Integer, ForeignKey("dates.id", ondelete="CASCADE"))
    master_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    user = relationship("User", foreign_keys=[user_id], lazy="joined")
    date = relationship("Date", back_populates="bookings", lazy="joined")
    service = relationship("Service", lazy="joined")
    time = relationship("Time", back_populates="bookings", lazy="joined")

    def __str__(self):
        return f"Час: {self.time} | Створено в: {self.created_at}"
