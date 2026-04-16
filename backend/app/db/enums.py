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
    PENDING = "PENDING"        # 已预订/待确认
    CONFIRMED = "CONFIRMED"    # 已确认（已支付或锁房）
    CHECKED_IN = "CHECKED_IN"  # 已入住
    CANCELLED = "CANCELLED"    # 已取消
    REFUNDED = "REFUNDED"      # 已退款


class RoleEnum(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    GUEST = "guest"