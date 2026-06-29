import asyncio
import json
from typing import Any

from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models, redis_client


ROOM_CACHE_TTL_SECONDS = 300
ROOM_CACHE_TIMEOUT_SECONDS = 0.1
ROOMS_ALL_CACHE_KEY = "cache:rooms:all"


class RoomCache:
    def __init__(
        self,
        client=redis_client,
        ttl_seconds: int = ROOM_CACHE_TTL_SECONDS,
        timeout_seconds: float = ROOM_CACHE_TIMEOUT_SECONDS,
    ):
        self.client = client
        self.ttl_seconds = ttl_seconds
        self.timeout_seconds = timeout_seconds

    def room_number_key(self, room_number: str) -> str:
        return f"cache:room:number:{room_number}"

    def room_id_key(self, room_id: int) -> str:
        return f"cache:room:id:{room_id}"

    def serialize_room(self, room: models.Room) -> dict[str, Any]:
        return {
            "id": room.id,
            "room_number": room.room_number,
            "type_": room.type_.value if room.type_ else None,
            "price": float(room.price),
        }

    async def get_json(self, key: str):
        try:
            value = await asyncio.wait_for(
                self.client.get(key),
                timeout=self.timeout_seconds,
            )
        except (RedisError, TimeoutError):
            return None

        if not value:
            return None

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None

    async def set_json(self, key: str, value):
        try:
            await asyncio.wait_for(
                self.client.set(
                    key,
                    json.dumps(value),
                    ex=self.ttl_seconds,
                ),
                timeout=self.timeout_seconds,
            )
        except (RedisError, TimeoutError):
            return

    async def cache_room(self, room_data: dict[str, Any]):
        await self.set_json(self.room_number_key(room_data["room_number"]), room_data)
        await self.set_json(self.room_id_key(room_data["id"]), room_data)

    async def invalidate(self, room_id: int | None = None, room_number: str | None = None):
        keys = [ROOMS_ALL_CACHE_KEY]
        if room_id is not None:
            keys.append(self.room_id_key(room_id))
        if room_number is not None:
            keys.append(self.room_number_key(room_number))

        try:
            await asyncio.wait_for(
                self.client.delete(*keys),
                timeout=self.timeout_seconds,
            )
        except (RedisError, TimeoutError):
            return

    async def get_room_by_number(self, db: AsyncSession, room_number: str):
        cached = await self.get_json(self.room_number_key(room_number))
        if cached:
            return cached

        result = await db.execute(
            select(models.Room).where(models.Room.room_number == room_number)
        )
        room = result.scalar_one_or_none()
        if room is None:
            return None

        room_data = self.serialize_room(room)
        await self.cache_room(room_data)
        return room_data

    async def get_room_by_id(self, db: AsyncSession, room_id: int):
        cached = await self.get_json(self.room_id_key(room_id))
        if cached:
            return cached

        result = await db.execute(select(models.Room).where(models.Room.id == room_id))
        room = result.scalar_one_or_none()
        if room is None:
            return None

        room_data = self.serialize_room(room)
        await self.cache_room(room_data)
        return room_data

    async def get_all_rooms(self, db: AsyncSession):
        cached = await self.get_json(ROOMS_ALL_CACHE_KEY)
        if cached is not None:
            return cached

        result = await db.execute(select(models.Room).order_by(models.Room.room_number))
        rooms = [self.serialize_room(room) for room in result.scalars().all()]
        await self.set_json(ROOMS_ALL_CACHE_KEY, rooms)
        return rooms


room_cache = RoomCache()
