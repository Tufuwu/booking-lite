from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
import services
from app.db import get_db
from app.core.permissions import require_permission

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("")
async def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:create"))
):
    return await services.create_order(db, order, current_user)

@router.get("/{order_id}")
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:read"))
):
    return await services.get_order(db, order_id, current_user)

@router.get("")
async def list_orders(
    user_id: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:list"))
):
    return await services.list_orders(db, user_id, status, current_user)

@router.post("/{order_id}/confirm")
async def confirm_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:update"))
):
    return await services.confirm_order(db, order_id, current_user)


@router.post("/{order_id}/check-in")
async def check_in_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:update"))
):
    return await services.check_in_order(db, order_id, current_user)


@router.post("/{order_id}/check-out")
async def check_out_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:update"))
):
    return await services.check_out_order(db, order_id, current_user)

@router.post("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:update"))
):
    return await services.cancel_order(db, order_id, current_user)


@router.post("/{order_id}/refund")
async def refund_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:refund"))
):
    return await services.refund_order(db, order_id, current_user)


@router.post("/{order_id}/extend")
async def extend_order(
    order_id: int,
    payload: schemas.OrderExtend,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:update"))
):
    return await services.extend_order(db, order_id, payload.extra_days, current_user)


@router.post("/{order_id}/recalculate")
async def recalculate_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("order:update"))
):
    return await services.recalculate_order(db, order_id, current_user)