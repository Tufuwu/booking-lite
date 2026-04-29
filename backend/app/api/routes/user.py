from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db import get_db
from app.deps.auth import get_current_user
from app import services
from app.crud import users
from app.db import models
from app.services import order as order_services

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)],
)


def get_current_user_id(current_user: dict) -> int:
    user_id = current_user.get("id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return user_id


async def get_current_db_user(
    db: AsyncSession,
    current_user: dict,
) -> models.User:
    user_id = get_current_user_id(current_user)
    db_user = await users.get_by_user_id(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return db_user


@router.post("/orders")
async def create_order(
    order: schemas.OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_user = await get_current_db_user(db, current_user)
    return await order_services.create_order(db, order, db_user)


@router.get("/orders")
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = get_current_user_id(current_user)

    return await order_services.list_orders(
        db,
        user_id=user_id,
        status=None,
        user=current_user,
    )


@router.post("/orders/{order_id}/confirm")
async def confirm_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = get_current_user_id(current_user)
    return await order_services.confirm_own_order(db, order_id, user_id)


@router.get("/rooms")
async def get_all_rooms(db: AsyncSession = Depends(get_db)):
    return await services.get_all_rooms(db)

