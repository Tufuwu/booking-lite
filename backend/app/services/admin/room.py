from sqlalchemy.orm import Session

from app import schemas
from app.db import models
from app.repository.room_repository import rooms


async def create_room(db: Session, room: schemas.RoomCreate):
    is_room_exist: models.Room = await rooms.get_by_room_number(db, room.room_number)
    if is_room_exist:
        return None
    new_room = models.Room(
        room_number=room.room_number,
        type_=room.type_,
        price=room.price
    )
    return await rooms.create_room(db, new_room)


async def delete_room(db: Session, room_number: str):
    room = await rooms.get_by_room_number(db, room_number)
    if not room:
        return None
    await rooms.delete_room(db, room)
    return True

async def get_all_rooms(db: Session):
    return await rooms.get_all_rooms(db)