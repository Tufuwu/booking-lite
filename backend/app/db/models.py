from datetime import datetime
from typing import List

from sqlalchemy import (
    String, Float, ForeignKey, DateTime, Enum,
    Table, Column, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import RoomType, RoomStatus, OrderStatus


# -------------------- association table --------------------
role_permission_table = Table(
    "role_permission_table",
    Base.metadata,
    Column("role_id", ForeignKey("role_table.id")),
    Column("permission_id", ForeignKey("permission_table.id"))
)


# -------------------- Admin --------------------
class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), index=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    identity_number: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    hashed_password: Mapped[str] = mapped_column(String(255))

    role_id: Mapped[int] = mapped_column(ForeignKey("role_table.id"))

    # FIX: async-safe loading
    role: Mapped["Role"] = relationship(
        back_populates="users",
        lazy="selectin"
    )

    orders: Mapped[List["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


# -------------------- Role --------------------
class Role(Base):
    __tablename__ = "role_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[List["User"]] = relationship(
        back_populates="role",
        lazy="selectin"
    )

    permissions: Mapped[List["Permission"]] = relationship(
        secondary="role_permission_table",
        back_populates="roles",
        lazy="selectin"   # ⭐关键修复点（你报错来源）
    )


# -------------------- Permission --------------------
class Permission(Base):
    __tablename__ = "permission_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    code: Mapped[str] = mapped_column(String(100), unique=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary="role_permission_table",
        back_populates="permissions",
        lazy="selectin"
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

    orders: Mapped[List["Order"]] = relationship(
        back_populates="room",
        lazy="selectin"
    )


# -------------------- Order --------------------
class Order(Base):
    __tablename__ = "order_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("room_table.id"))

    user: Mapped["User"] = relationship(
        back_populates="orders",
        lazy="selectin"
    )

    room: Mapped["Room"] = relationship(
        back_populates="orders",
        lazy="selectin"
    )

    check_in_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    stay_length: Mapped[int] = mapped_column()

    expense: Mapped[float] = mapped_column(Float)

    # -------------------- state machine --------------------
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True,
    )

    # -------------------- timestamps --------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # -------------------- constraints --------------------
    __table_args__ = (
        CheckConstraint("stay_length > 0", name="ck_stay_length_positive"),
        CheckConstraint("expense >= 0", name="ck_expense_non_negative"),
    )

    # -------------------- FSM core --------------------
    def set_status(self, new_status: OrderStatus):
        self.status = new_status

    def mark_confirmed(self):
        self.status = OrderStatus.CONFIRMED

    def mark_checked_in(self):
        self.status = OrderStatus.CHECKED_IN

    def mark_cancelled(self):
        self.status = OrderStatus.CANCELLED

    def mark_refunded(self):
        self.status = OrderStatus.REFUNDED
