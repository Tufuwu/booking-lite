from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app import core
from app import schemas
from app.db import models
from app.crud import users, roles, rooms



async def login_user(db: AsyncSession, form_data):

    user: models.Admin = await users.get_by_user_name(db, form_data.username)

    if not user:
        return None
    is_vaild_admin = core.security.verify_password(form_data.password, user.hashed_password)
    if not is_vaild_admin:
        return None
    return {
        "id": user.id,
        "name": user.name,
        "role": user.role.name,
    }


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    is_user_exist: models.Admin = await users.get_by_user_name(db, user.identity_number)

    if is_user_exist:
        return None
    role = await roles.get_by_name(db, user.role)
    if not role:
        raise ValueError("Role not found")
    admin_role = await roles.get_by_name(db, user.role)
    if not admin_role:
        raise ValueError("Admin role not initialized")
    hashed_password = core.security.hash_password(user.password)

    new_user = models.User(
        name=user.name,
        phone_number=user.phone_number,
        identity_number=user.identity_number,
        hashed_password=hashed_password,
        role_id=role.id
    )
    return await users.create_user(db, new_user)


async def get_me(db: AsyncSession, current_user: dict):
    user = await users.get_by_user_id(db, current_user["id"])

    if not user:
        raise HTTPException(401)

    return {
        "id": user.id,
        "name": user.name,
        "role_id": user.role_id,

        "role": {
            "id": user.role.id,
            "name": user.role.name,
            "permissions": [
                {
                    "id": p.id,
                    "name": p.name,
                    "code": p.code
                }
                for p in (user.role.permissions if user.role else [])
            ]
        } if user.role else None
    }


def serialize_room(room: models.Room):
    return {
        "id": room.id,
        "room_number": room.room_number,
        "type_": room.type_.value if room.type_ else None,
        "price": room.price,
        "room_status": room.room_status.value if room.room_status else None,
    }

def serialize_user(user: models.User):
    return {
        "id": user.id,
        "name": user.name,
        "room_number": user.phone_number,
        "order": user.orders
    }
async def create_room(db: AsyncSession, room: schemas.RoomCreate):
    existing_room = await rooms.get_by_room_number(db, room.room_number)
    if existing_room:
        raise HTTPException(status_code=409, detail="Room already exists")

    new_room = models.Room(
        room_number=room.room_number,
        type_=room.type_,
        price=float(room.price),
    )
    created_room = await rooms.create_room(db, new_room)
    return serialize_room(created_room)


async def delete_room(db: AsyncSession, room_number: str):
    room = await rooms.get_by_room_number(db, room_number)
    if not room:
        return False

    await rooms.delete_room(db, room)
    return True


async def get_all_rooms(db: AsyncSession):
    room_list = await rooms.get_all_rooms(db)
    return [serialize_room(room) for room in room_list]


async def get_all_users(db: AsyncSession):
    user_list = await users.get_all_users(db)
    return [serialize_user(user) for user in user_list]