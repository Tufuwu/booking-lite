from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException

from app import schemas
from app.db import models
from backend.app.crud.permissions_crud import orders,rooms
from app.db.enums import OrderStatus, RoomStatus

ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.CHECKED_IN, OrderStatus.CANCELLED},
    OrderStatus.CHECKED_IN: {OrderStatus.REFUNDED, OrderStatus.COMPLETED},
    OrderStatus.CANCELLED: {OrderStatus.REFUNDED},
    OrderStatus.REFUNDED: set(),
}


def validate_transition(order, new_status: OrderStatus):
    allowed = ALLOWED_TRANSITIONS.get(order.status, set())

    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"{order.status} -> {new_status} not allowed"
        )
    
async def create_order(db: Session, order_in: schemas.OrderCreate, user):
    room = rooms.get_by_id(db, order_in.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.room_status != RoomStatus.VACANT:
        raise HTTPException(
            status_code=400,
            detail=f"Room not available, current status: {room.room_status}"
        )

    order = models.Order(
        user_id=user.id,
        room_id=room.id,
        stay_length=order_in.stay_length,
        status=OrderStatus.PENDING,
        expense=(room.price * order_in.stay_length)
    )

    db.add(order)

    room.room_status = RoomStatus.RESERVED

    db.commit()
    db.refresh(order)

    return order



async def confirm_order(db: Session, order_id: int, user):
    order = orders.get_by_id(db, order_id)

    validate_transition(order, OrderStatus.CONFIRMED)

    order.mark_confirmed()
 
    db.commit()
    return order


async def check_in_order(db: Session, order_id: int, user):
    order = orders.get_by_id(db, order_id)

    validate_transition(order, OrderStatus.CHECKED_IN)

    order.mark_checked_in()

    # side effect 在 service 统一处理
    order.room.room_status = RoomStatus.OCCUPIED

    db.commit()
    return order

async def cancel_order(db: Session, order_id: int, user):
    order = orders.get_by_id(db, order_id)

    validate_transition(order, OrderStatus.CANCELLED)

    order.mark_cancelled()

    order.room.room_status = RoomStatus.VACANT

    db.commit()
    return order

async def refund_order(db: Session, order_id: int, user):
    order = orders.get_by_id(db, order_id)

    validate_transition(order, OrderStatus.REFUNDED)

    order.mark_refunded()

    db.commit()
    return order

async def check_out_order(db: Session, order_id: int, user):
    order = orders.get_by_id(db, order_id)

    validate_transition(order, OrderStatus.COMPLETED)

    order.set_status(OrderStatus.COMPLETED)

    order.room.room_status = RoomStatus.VACANT

    db.commit()
    return order