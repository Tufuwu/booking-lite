from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import (
    String,
    Float,
    ForeignKey,
    DateTime,
    Date,
    Enum,
    Table,
    Column,
    CheckConstraint,
    UniqueConstraint,
    Integer,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import RoomType, OrderStatus


# -------------------- association table --------------------
role_permission_table = Table(
    "role_permission_table",
    Base.metadata,
    Column("role_id", ForeignKey("role_table.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission_table.id"), primary_key=True),
)


# -------------------- User --------------------
class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), index=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    identity_number: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    hashed_password: Mapped[str] = mapped_column(String(255))

    role_id: Mapped[int] = mapped_column(ForeignKey("role_table.id"), index=True)

    role: Mapped["Role"] = relationship(
        back_populates="users",
        lazy="selectin",
    )

    orders: Mapped[List["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


# -------------------- Role --------------------
class Role(Base):
    __tablename__ = "role_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(
        back_populates="role",
        lazy="selectin",
    )

    permissions: Mapped[List["Permission"]] = relationship(
        secondary=role_permission_table,
        back_populates="roles",
        lazy="selectin",
    )


# -------------------- Permission --------------------
class Permission(Base):
    __tablename__ = "permission_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    roles: Mapped[List["Role"]] = relationship(
        secondary=role_permission_table,
        back_populates="permissions",
        lazy="selectin",
    )


# -------------------- Room --------------------
class Room(Base):
    __tablename__ = "room_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    room_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
    )

    type_: Mapped[RoomType] = mapped_column(
        Enum(RoomType),
        index=True,
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    orders: Mapped[List["Order"]] = relationship(
        back_populates="room",
        lazy="selectin",
    )

    availability: Mapped[List["RoomAvailability"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_room_price_non_negative"),
    )

# -------------------- Order --------------------
class Order(Base):
    __tablename__ = "order_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_table.id"),
        index=True,
        nullable=False,
    )

    room_id: Mapped[int] = mapped_column(
        ForeignKey("room_table.id"),
        index=True,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="orders",
        lazy="selectin",
    )

    room: Mapped["Room"] = relationship(
        back_populates="orders",
        lazy="selectin",
    )

    check_in_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    check_out_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    stay_length: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    expense: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True,
    )

    room_dates: Mapped[List["RoomAvailability"]] = relationship(
        back_populates="order",
        lazy="selectin",
    )

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

    __table_args__ = (
        CheckConstraint(
            "check_out_date > check_in_date",
            name="ck_checkout_after_checkin",
        ),
        CheckConstraint(
            "stay_length > 0",
            name="ck_stay_length_positive",
        ),
        CheckConstraint(
            "expense >= 0",
            name="ck_expense_non_negative",
        ),
    )

    def set_status(self, new_status: OrderStatus):
        self.status = new_status

    def mark_pending(self):
        self.status = OrderStatus.PENDING

    def mark_confirmed(self):
        self.status = OrderStatus.CONFIRMED

    def mark_checked_in(self):
        self.status = OrderStatus.CHECKED_IN

    def mark_cancelled(self):
        self.status = OrderStatus.CANCELLED

    def mark_cancelled_unpaid(self):
        self.status = OrderStatus.CANCELLED_UNPAID

    def mark_cancelled_paid(self):
        self.status = OrderStatus.CANCELLED_PAID

    def mark_refunded(self):
        self.status = OrderStatus.REFUNDED


# -------------------- Room Availability --------------------
class RoomAvailability(Base):
    __tablename__ = "room_availability_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    room_id: Mapped[int] = mapped_column(
        ForeignKey("room_table.id"),
        nullable=False,
        index=True,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )

    order_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("order_table.id"),
        nullable=True,
        index=True,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    room: Mapped["Room"] = relationship(
        back_populates="availability",
        lazy="selectin",
    )

    order: Mapped[Optional["Order"]] = relationship(
        back_populates="room_dates",
        lazy="selectin",
    )

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

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "date",
            name="uq_room_availability_room_date",
        ),
    )
