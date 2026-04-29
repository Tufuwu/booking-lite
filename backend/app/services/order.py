from datetime import date, timedelta

from fastapi import HTTPException
from redis.exceptions import RedisError
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import schemas
from app.core.locks import redis_multi_lock
from app.db import redis_client
from app.db import models
from app.db.enums import OrderStatus


ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED_UNPAID},
    OrderStatus.CONFIRMED: {OrderStatus.CHECKED_IN, OrderStatus.CANCELLED_PAID},
    OrderStatus.CHECKED_IN: {OrderStatus.COMPLETED, OrderStatus.REFUNDED},
    OrderStatus.CANCELLED_UNPAID: set(),
    OrderStatus.CANCELLED_PAID: {OrderStatus.REFUNDED},
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
        "check_in_date": order.check_in_date,
        "check_out_date": order.check_out_date,
        "check_in_time": order.check_in_date,
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
        } if order.room else None,
        "room_dates": [
            {
                "date": item.date,
                "is_available": item.is_available,
                "version": item.version,
            }
            for item in (order.room_dates or [])
        ],
    }


def iter_stay_dates(check_in_date: date, check_out_date: date):
    current = check_in_date
    while current < check_out_date:
        yield current
        current += timedelta(days=1)


def room_date_lock_keys(room_id: int, dates: list[date]):
    return [f"lock:room:{room_id}:date:{item.isoformat()}" for item in dates]


def room_date_cache_key(room_id: int, day: date):
    return f"cache:room:{room_id}:date:{day.isoformat()}:available"


async def set_availability_cache(room_id: int, dates: list[date], is_available: bool):
    value = "1" if is_available else "0"
    try:
        for day in dates:
            await redis_client.set(room_date_cache_key(room_id, day), value, ex=3600)
    except RedisError:
        # Redis is an acceleration and locking layer; database state remains authoritative.
        return


async def get_room_availability_rows(
    db: AsyncSession,
    room_id: int,
    dates: list[date],
):
    result = await db.execute(
        select(models.RoomAvailability).where(
            models.RoomAvailability.room_id == room_id,
            models.RoomAvailability.date.in_(dates),
        )
    )
    return {item.date: item for item in result.scalars().all()}


async def ensure_dates_available(
    db: AsyncSession,
    room_id: int,
    dates: list[date],
):
    availability_by_date = await get_room_availability_rows(db, room_id, dates)

    unavailable_dates = [
        day.isoformat()
        for day, item in availability_by_date.items()
        if not item.is_available
    ]

    if unavailable_dates:
        raise HTTPException(
            status_code=409,
            detail=f"Room not available on: {', '.join(unavailable_dates)}",
        )

    return availability_by_date


async def reserve_room_dates(
    db: AsyncSession,
    order: models.Order,
    dates: list[date],
):
    availability_by_date = await ensure_dates_available(db, order.room_id, dates)

    for day in dates:
        availability = availability_by_date.get(day)
        if availability is None:
            availability = models.RoomAvailability(
                room_id=order.room_id,
                date=day,
                is_available=False,
                order_id=order.id,
                version=1,
            )
            db.add(availability)
            continue

        result = await db.execute(
            update(models.RoomAvailability)
            .where(
                models.RoomAvailability.id == availability.id,
                models.RoomAvailability.version == availability.version,
                models.RoomAvailability.is_available.is_(True),
            )
            .values(
                is_available=False,
                order_id=order.id,
                version=models.RoomAvailability.version + 1,
            )
            .execution_options(synchronize_session=False)
        )

        if result.rowcount != 1:
            raise HTTPException(
                status_code=409,
                detail=f"Room availability changed on: {day.isoformat()}",
            )


async def release_room_dates(db: AsyncSession, order: models.Order):
    dates = list(iter_stay_dates(order.check_in_date, order.check_out_date))
    result = await db.execute(
        select(models.RoomAvailability).where(
            models.RoomAvailability.room_id == order.room_id,
            models.RoomAvailability.order_id == order.id,
            models.RoomAvailability.date.in_(dates),
        )
    )

    availability_rows = result.scalars().all()

    if len(availability_rows) != len(dates):
        raise HTTPException(
            status_code=409,
            detail="Room availability records changed, please retry",
        )

    for availability in availability_rows:
        result = await db.execute(
            update(models.RoomAvailability)
            .where(
                models.RoomAvailability.id == availability.id,
                models.RoomAvailability.version == availability.version,
                models.RoomAvailability.order_id == order.id,
                models.RoomAvailability.is_available.is_(False),
            )
            .values(
                is_available=True,
                order_id=None,
                version=models.RoomAvailability.version + 1,
            )
            .execution_options(synchronize_session=False)
        )

        if result.rowcount != 1:
            raise HTTPException(
                status_code=409,
                detail=f"Room availability changed on: {availability.date.isoformat()}",
            )

    return dates


async def get_order_model(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(models.Order)
        .options(
            selectinload(models.Order.user),
            selectinload(models.Order.room),
            selectinload(models.Order.room_dates),
        )
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

    if order_in.check_out_date is None or order_in.stay_length is None:
        raise HTTPException(status_code=400, detail="Invalid order dates")

    stay_dates = list(iter_stay_dates(order_in.check_in_date, order_in.check_out_date))
    lock_keys = room_date_lock_keys(room.id, stay_dates)

    try:
        async with redis_multi_lock(redis_client, lock_keys):
            order = models.Order(
                user_id=user.id,
                room_id=room.id,
                check_in_date=order_in.check_in_date,
                check_out_date=order_in.check_out_date,
                stay_length=order_in.stay_length,
                status=OrderStatus.PENDING,
                expense=room.price * order_in.stay_length,
            )

            db.add(order)
            await db.flush()
            await reserve_room_dates(db, order, stay_dates)

            await db.commit()
            db.expire_all()
            await set_availability_cache(room.id, stay_dates, False)
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Room availability changed, please retry")

    order = await get_order_model(db, order.id)
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
        .options(
            selectinload(models.Order.user),
            selectinload(models.Order.room),
            selectinload(models.Order.room_dates),
        )
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


async def confirm_own_order(db: AsyncSession, order_id: int, user_id: int):
    order = await get_order_model(db, order_id)
    if order.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Order does not belong to current user",
        )

    validate_transition(order, OrderStatus.CONFIRMED)

    order.mark_confirmed()
    await db.commit()
    await db.refresh(order)
    return serialize_order(order)


async def check_in_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    validate_transition(order, OrderStatus.CHECKED_IN)

    order.mark_checked_in()

    await db.commit()
    await db.refresh(order)
    return serialize_order(order)


async def cancel_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)

    if order.status == OrderStatus.PENDING:
        new_status = OrderStatus.CANCELLED_UNPAID
    elif order.status == OrderStatus.CONFIRMED:
        new_status = OrderStatus.CANCELLED_PAID
    else:
        raise HTTPException(
            status_code=400,
            detail=f"{order.status} -> cancelled not allowed",
        )

    validate_transition(order, new_status)
    order.set_status(new_status)
    released_dates = await release_room_dates(db, order)

    await db.commit()
    await set_availability_cache(order.room_id, released_dates, True)
    db.expire_all()
    order = await get_order_model(db, order_id)
    return serialize_order(order)


async def refund_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    validate_transition(order, OrderStatus.REFUNDED)

    order.mark_refunded()
    released_dates = await release_room_dates(db, order)

    await db.commit()
    await set_availability_cache(order.room_id, released_dates, True)
    db.expire_all()
    order = await get_order_model(db, order_id)
    return serialize_order(order)


async def check_out_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    validate_transition(order, OrderStatus.COMPLETED)

    order.set_status(OrderStatus.COMPLETED)
    released_dates = await release_room_dates(db, order)

    await db.commit()
    await set_availability_cache(order.room_id, released_dates, True)
    db.expire_all()
    order = await get_order_model(db, order_id)
    return serialize_order(order)


async def extend_order(
    db: AsyncSession,
    order_id: int,
    extra_days: int,
    user: models.User,
):
    order = await get_order_model(db, order_id)
    old_check_out_date = order.check_out_date
    new_check_out_date = order.check_out_date + timedelta(days=extra_days)
    added_dates = list(iter_stay_dates(old_check_out_date, new_check_out_date))

    try:
        async with redis_multi_lock(redis_client, room_date_lock_keys(order.room_id, added_dates)):
            order.check_out_date = new_check_out_date
            order.stay_length += extra_days
            order.expense = order.room.price * order.stay_length
            await reserve_room_dates(db, order, added_dates)

            await db.commit()
            db.expire_all()
            await set_availability_cache(order.room_id, added_dates, False)
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Room availability changed, please retry")

    order = await get_order_model(db, order_id)
    return serialize_order(order)


async def recalculate_order(db: AsyncSession, order_id: int, user: models.User):
    order = await get_order_model(db, order_id)
    order.expense = order.room.price * order.stay_length

    await db.commit()
    await db.refresh(order)
    return serialize_order(order)
