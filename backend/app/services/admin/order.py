from sqlalchemy.orm import Session
from typing import Optional

from app import schemas
from app.db import models
from app.repository.room_repository import orders,rooms
from app.db import enums


async def create_order(db: Session, order: schemas.OrderCreate):
    order_room = await rooms.get_by_room_number(db, order.room_id)
    expense = order_room.price * order.stay_nights
    new_order = models.Order(
        user_id=order.user_id,
        room_number=order.room_id,
        check_in_date=order.check_in_date,
        stay_nights=order.stay_nights,
        expense=expense,
        payment_status=enums.PaymentStatus.UNPAID
    )
    return await orders.create_order(db, new_order)


async def get_order_id(
    db: Session, 
    user_id: Optional[int] = None,
    room_id: Optional[int] = None,
    check_in_time_min: Optional[str] = None,
    stay_nights: Optional[str] = None,
    payment_status: Optional[str] = None
    ):
    criterion: list = []
    if user_id is not None:
        criterion.append(models.Order.user_id == user_id)
    if room_id is not None:
        criterion.append(models.Order.room_id == room_id)
    if check_in_time_min is not None:
        criterion.append(models.Order.check_in_time >= check_in_time_min)
    if stay_nights is not None:
        criterion.append(models.Order.stay_nights == stay_nights)
    if payment_status is not None:
        criterion.append(models.Order.payment_status == payment_status)
    return await orders.get_by_criterion(db, criterion)