from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import models

class PermissionCrud:
    async def get_by_code(self, db: Session, code: str):
        result = await db.execute(
            select(models.Permission).where(models.Permission.code == code)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: Session):
        result = await db.execute(select(models.Permission))
        return result.scalars().all()
    
permissions = PermissionCrud()