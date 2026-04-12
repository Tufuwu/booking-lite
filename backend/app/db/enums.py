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


class PaymentStatus(str, Enum):
    UNPAID = "unpaid"
    PAID = "paid"