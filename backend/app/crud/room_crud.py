from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models


class RoomCrud:
    async def get_by_room_number(self, db: AsyncSession, room_number: str):
        result = await db.execute(
            select(models.Room).filter(models.Room.room_number == room_number)
        )
        return result.scalar_one_or_none()

    async def get_all_rooms(self, db: AsyncSession):
        result = await db.execute(
            select(models.Room).order_by(models.Room.room_number)
        )
        return result.scalars().all()

    async def create_room(self, db: AsyncSession, room: models.Room):
        db.add(room)
        await db.commit()
        await db.refresh(room)
        return room

    async def delete_room(self, db: AsyncSession, room: models.Room) -> None:
        await db.delete(room)
        await db.commit()


rooms = RoomCrud()
