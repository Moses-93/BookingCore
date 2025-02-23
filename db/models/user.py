from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean,
    Text,
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey,
    func,
    Table,
    BigInteger,
)
from .base import Base

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

    def __str__(self):
        return f"Name: {self.name} | UserID: {self.chat_id}"
