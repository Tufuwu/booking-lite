import asyncio
import uuid
from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncIterator

from fastapi import HTTPException
from redis.asyncio import Redis
from redis.exceptions import RedisError


RELEASE_LOCK_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
"""


@asynccontextmanager
async def redis_lock(
    redis_client: Redis,
    key: str,
    ttl_seconds: int = 15,
    wait_timeout_seconds: float = 3,
    retry_interval_seconds: float = 0.05,
) -> AsyncIterator[None]:
    token = str(uuid.uuid4())
    deadline = asyncio.get_running_loop().time() + wait_timeout_seconds
    acquired = False

    try:
        while asyncio.get_running_loop().time() < deadline:
            acquired = bool(await redis_client.set(key, token, nx=True, ex=ttl_seconds))
            if acquired:
                break
            await asyncio.sleep(retry_interval_seconds)
    except RedisError:
        raise HTTPException(status_code=503, detail="Room lock service unavailable")

    if not acquired:
        raise HTTPException(status_code=409, detail="Room is being booked, please retry")

    try:
        yield
    finally:
        try:
            await redis_client.eval(RELEASE_LOCK_SCRIPT, 1, key, token)
        except RedisError:
            pass


@asynccontextmanager
async def redis_multi_lock(
    redis_client: Redis,
    keys: list[str],
    ttl_seconds: int = 15,
) -> AsyncIterator[None]:
    acquired: list[AsyncContextManager[None]] = []

    try:
        for key in sorted(set(keys)):
            lock = redis_lock(redis_client, key, ttl_seconds=ttl_seconds)
            await lock.__aenter__()
            acquired.append(lock)
        yield
    finally:
        for lock in reversed(acquired):
            await lock.__aexit__(None, None, None)
