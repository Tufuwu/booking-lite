from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import schemas
from app.db import models
from app.db.enums import OrderStatus, RoomStatus


ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.CHECKED_IN, OrderStatus.CANCELLED},
    OrderStatus.CHECKED_IN: {OrderStatus.REFUNDED, OrderStatus.COMPLETED},
    OrderStatus.CANCELLED: {OrderStatus.REFUNDED},
    OrderStatus.COMPLETED: set(),
    OrderStatus.REFUNDED: set(),
}


def validate_transition(order: models.Order, new_status: OrderStatus):
    allowed = ALLOWED_TRANSITIONS.get(order.status, set())

    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"{order.status} -> {new_status} not allowed",
        )


def serialize_order(order: models.Order):
    return {
        "id": order.id,
        "user_id": order.user_id,
        "room_id": order.room_id,
        "check_in_time": order.check_in_time,
        "stay_length": order.stay_length,
        "expense": order.expense,
        "status": order.status.value if order.status else None,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "user": {
            "id": order.user.id,
            "name": order.user.name,
            "phone_number": order.user.phone_number,
            "identity_number": order.user.identity_number,
        } if order.user else None,
        "room": {
            "id": order.room.id,
            "room_number": order.room.room_number,
            "type_": order.room.type_.value if order.room.type_ else None,
            "price": order.room.price,
            "room_status": order.room.room_status.value if order.room.room_status else None,
        } if order.room else None,
    }


async def get_order_model(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.user), selectinload(models.Order.room))
        .where(models.Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


async def create_order(db: AsyncSession, order_in: schemas.OrderCreate, user: models.User):
    if order_in.room_number:
        result = await db.execute(
            select(models.Room).where(models.Room.room_number == order_in.room_number)
        )
    else:
        result = await db.execute(select(models.Room).where(models.Room.id == order_in.room_id))

    room = result.scalar_one_or_none()

    if room is None:
        room_ref = order_in.room_number if order_in.room_number else order_in.room_id
        raise HTTPException(status_code=404, detail=f"Room not found: {room_ref}")

    if room.room_status != RoomStatus.VACANT:
        raise HTTPException(
            status_code=400,
            detail=f"Room not available, current status: {room.room_status.value}",
        )

    order = models.Order(
        user_id=user.id,
        room_id=room.id,
        stay_length=order_in.stay_length,
        status=OrderStatus.PENDING,
        expense=room.price * order_in.stay_length,
    )

    db.add(order)
    room.room_status = RoomStatus.RESERVED

    await db.commit()
    await db.refresh(order)

    order.user = user
    order.room = room
    return serialize_order(order)


async def get_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    return serialize_order(order)


async def list_orders(
    db: AsyncSession,
    user_id: int | None,
    status: str | None,
    user: models.User,
):
    criteria = []

    if user_id is not None:
        criteria.append(models.Order.user_id == user_id)

    if status:
        try:
            order_status = OrderStatus(status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid order status")
        criteria.append(models.Order.status == order_status)

    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.user), selectinload(models.Order.room))
        .where(*criteria)
        .order_by(models.Order.created_at.desc())
    )

    return [serialize_order(order) for order in result.scalars().all()]


async def confirm_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    validate_transition(order, OrderStatus.CONFIRMED)

    order.mark_confirmed()
    await db.commit()
    await db.refresh(order)
    return serialize_order(order)


async def check_in_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    validate_transition(order, OrderStatus.CHECKED_IN)

    order.mark_checked_in()
    order.room.room_status = RoomStatus.OCCUPIED

    await db.commit()
    await db.refresh(order)
    return serialize_order(order)


async def cancel_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    validate_transition(order, OrderStatus.CANCELLED)

    order.mark_cancelled()
    order.room.room_status = RoomStatus.VACANT

    await db.commit()
    await db.refresh(order)
    return serialize_order(order)


async def refund_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    validate_transition(order, OrderStatus.REFUNDED)

    order.mark_refunded()

    await db.commit()
    await db.refresh(order)
    return serialize_order(order)


async def check_out_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    validate_transition(order, OrderStatus.COMPLETED)

    order.set_status(OrderStatus.COMPLETED)
    order.room.room_status = RoomStatus.VACANT

    await db.commit()
    await db.refresh(order)
    return serialize_order(order)


async def extend_order(
    db: AsyncSession,
    order_id: int,
    extra_days: int,
    user: models.User,
):
    order = await get_order_model(db, order_id)
    order.stay_length += extra_days
    order.expense = order.room.price * order.stay_length

    await db.commit()
    await db.refresh(order)
    return serialize_order(order)


async def recalculate_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    order.expense = order.room.price * order.stay_length

    await db.commit()
    await db.refresh(order)
    return serialize_order(order)
