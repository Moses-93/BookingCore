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
    JSON,
)

Base = declarative_base()


class Date(Base):
    __tablename__ = "dates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, unique=True)
    free = Column(Boolean, default=True, index=True)
    del_time = Column(DateTime, nullable=False)

    bookings = relationship("Booking", back_populates="date", lazy="joined")

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
    reminder_hours = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
    time_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    date_id = Column(Integer, ForeignKey("dates.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="bookings", lazy="joined")
    date = relationship("Date", back_populates="bookings", lazy="joined")
    service = relationship("Service", lazy="joined")

    def __str__(self):
        return f"Час: {self.time} | Створено в: {self.created_at}"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True)
    chat_id = Column(Integer, index=True, nullable=False, unique=True)
    role = Column(String(10), nullable=True, default="user")

    bookings = relationship("Booking", back_populates="user", lazy="joined")

    def __str__(self):
        return f"Name: {self.name} | UserID: {self.chat_id}"


class Time(Base):
    __tablename__ = "times"
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True, index=True)
    time = Column(Time, nullable=False)
    date_id = Column(Integer, ForeignKey("dates.id"), nullable=False)

    def __str__(self):
        return f"Час: {self.time}"


class BusinessInfo(Base):
    __tablename__ = "business_info"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(60), nullable=False)
    phone = Column(String(13), nullable=False)
    description = Column(String, nullable=True)
    working_hours = Column(JSON, nullable=False)
    google_maps_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __str__(self):
        return f"Назва: {self.name} | Адреса: {self.address} | Телефон: {self.phone}"
