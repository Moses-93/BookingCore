from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import (
    Boolean,
    Interval,
    Time,
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey,
    Date,
    func,
)

Base = declarative_base()


class Date(Base):
    __tablename__ = "dates"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    free = Column(Boolean, default=True, index=True)
    del_time = Column(DateTime, nullable=False)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    duration = Column(Interval, nullable=False)

    def __str__(self):
        return f"{self.name}: {self.price} грн."


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=True, index=True)
    time = Column(Time, nullable=False)
    reminder_hours = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
    name_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    date_id = Column(Integer, ForeignKey("dates.id", ondelete="CASCADE"))

    name = relationship("User", lazy="joined")
    date = relationship("Date", lazy="joined")
    service = relationship("Service", lazy="joined")

    def __str__(self):
        return f"Час: {self.time} | Створено в: {self.created_at}"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True)
    chat_id = Column(Integer, index=True, nullable=False, unique=True)
    admin = Column(Boolean, nullable=False, default=False)

    def __str__(self):
        return f"Name: {self.name} | UserID: {self.user_id}"
