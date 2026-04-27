from enum import Enum


class RoomType(str, Enum):
    SINGLE = "single"
    TWIN = "twin"
    FAMILY = "family"


class RoomStatus(str, Enum):
    VACANT = "vacant"
    OCCUPIED = "occupied"
    DIRTY = "dirty"
    RESERVED = "reserved"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class RoleEnum(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    GUEST = "guest"
