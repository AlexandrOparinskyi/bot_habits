from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)

    habits = relationship("Habit",
                          back_populates="owner",
                          lazy="selectin")


class Habit(Base):
    __tablename__ = "habits"

    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, nullable=False, default=True)
    frequency = Column(Integer, default=1, nullable=False)
    count_days = Column(Integer, default=0, nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)

    owner = relationship("User",
                         back_populates="habits",
                         lazy="selectin")
