import secrets
import json
import time
from app.db.redis import redis_client
from app.repository import admins
SESSION_EXPIRE = 7200

class SessionService:

    async def create_session(self, user: dict):
        session_id = secrets.token_urlsafe(32)

        data = {
            "user_id": user["job_number"],
            "role": user["role"],
            "created_at": int(time.time())
        }

        await redis_client.set(
            f"session:{session_id}",
            json.dumps(data),
            ex=SESSION_EXPIRE
        )

        return session_id

    async def get_session(self, session_id: str):
        key = f"session:{session_id}"
        data = await redis_client.get(key)
        if not data:
            return None

        # ⭐ 刷新过期时间（滑动过期）
        await redis_client.expire(key, SESSION_EXPIRE)

        return json.loads(data)
    
    async def delete_session(self, session_id):
        await redis_client.delete(f"session:{session_id}")

    async def get_user(self, db, current_admin):
        return await admins.get_by_job_number(db, current_admin['user_id'])