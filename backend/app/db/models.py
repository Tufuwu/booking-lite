from datetime import datetime
from typing import List

from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import RoomType, RoomStatus, PaymentStatus


# -------------------- Admin --------------------
class Admin(Base):
    __tablename__ = "admin_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))


# -------------------- User --------------------
class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    identity_number: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    # 关系
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


# -------------------- Room --------------------
class Room(Base):
    __tablename__ = "room_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)

    type_: Mapped[RoomType] = mapped_column(Enum(RoomType), index=True)
    price: Mapped[float] = mapped_column(Float)

    room_status: Mapped[RoomStatus] = mapped_column(
        Enum(RoomStatus),
        default=RoomStatus.VACANT,
        index=True
    )

    # 关系
    orders: Mapped[List["Order"]] = relationship(
        back_populates="room"
    )


# -------------------- Order --------------------
class Order(Base):
    __tablename__ = "order_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    # 外键
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("room_table.id"))

    # 关系
    user: Mapped["User"] = relationship(back_populates="orders")
    room: Mapped["Room"] = relationship(back_populates="orders")

    # 业务字段
    check_in_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    stay_length: Mapped[int] = mapped_column()  # 天数

    expense: Mapped[float] = mapped_column(Float)

    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.UNPAID
    )