from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import (
    Boolean,
    Text,
    Time,
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey,
    Date,
    func,
    Float,
    Table,
    BigInteger,
)

Base = declarative_base()


user_master_association = Table(
    "user_master_association",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "master_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True)
    phone_number = Column(Text, nullable=True, unique=True)
    chat_id = Column(BigInteger, index=True, nullable=False, unique=True)
    role = Column(String(10), nullable=True, default="client")
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=func.now())

    masters = relationship(
        "User",
        secondary=user_master_association,
        primaryjoin=id == user_master_association.c.user_id,
        secondaryjoin=id == user_master_association.c.master_id,
        backref="clients",
    )

    bookings = relationship("Booking", back_populates="user", lazy="joined")
    feedbacks = relationship("Feedback", back_populates="user", lazy="joined")

    def __str__(self):
        return f"Name: {self.name} | UserID: {self.chat_id}"


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    master_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __str__(self):
        return f"{self.name}: {self.price} грн."


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

    user = relationship(
        "User", foreign_keys=[user_id], back_populates="bookings", lazy="joined"
    )
    master = relationship("User", foreign_keys=[master_id], lazy="joined")
    date = relationship("Date", back_populates="bookings", lazy="joined")
    service = relationship("Service", lazy="joined")
    time = relationship("Time", back_populates="bookings", lazy="joined")

    def __str__(self):
        return f"Час: {self.time} | Створено в: {self.created_at}"


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

    def __str__(self):
        return f"Назва: {self.name} | Адреса: {self.address} | Телефон: {self.phone_number}"


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    master_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="feedbacks", lazy="joined")
    master = relationship("User", back_populates="feedbacks", lazy="joined")

    def __str__(self):
        return f"Ім'я: {self.user.name} | Рейтинг: {self.rating} | Коментар: {self.comment}"


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    duration_days = Column(Integer, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
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
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())

    master = relationship("User", back_populates="subscription", lazy="joined")
    plan = relationship(
        "SubscriptionPlan", back_populates="subscriptions", lazy="joined"
    )


# Створити таблицю
# Поля:
#     - master_id (FK → Users)
#     - plan_type (ENUM: free, monthly, yearly, promo)
#     - expires_at (TIMESTAMP)
#     - payment_status (ENUM: pending, success, failed)
#     - created_at (TIMESTAMP)

# Оновити:
# -  Додати поле is_active до таблиці masters
