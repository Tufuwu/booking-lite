from app.db import models
from sqlalchemy.orm import Session
from sqlalchemy import select


class RoleCrud:
    async def get_by_name(self, db: Session, name: str):
        result = await db.execute(select(models.Role).filter(models.Role.name == name)) 
        return result.scalar_one_or_none()



roles = RoleCrud()
