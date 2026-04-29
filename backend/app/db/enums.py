from enum import Enum


class RoomType(str, Enum):
    SINGLE = "single"
    TWIN = "twin"
    FAMILY = "family"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    CANCELLED_UNPAID = "CANCELLED_UNPAID"
    CANCELLED_PAID = "CANCELLED_PAID"
    REFUNDED = "REFUNDED"


class RoleEnum(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    GUEST = "guest"
