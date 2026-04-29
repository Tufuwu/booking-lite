
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import models


class UserCrud:
    async def get_by_user_phone_number(self, db: AsyncSession, phone_number: str):
        result = await db.execute(select(models.User).filter(models.User.phone_number == phone_number))
        return result.scalar_one_or_none()

    async def get_by_identity_number(self, db: AsyncSession, identity_number: str):
        result = await db.execute(
            select(models.User).filter(models.User.identity_number == identity_number)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(models.User).filter(models.User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_user_name(self, db: AsyncSession, name: str):
        result = await db.execute(select(models.User).filter(models.User.name == name))
        return result.scalar_one_or_none()

    async def get_orders_by_user(self, db: AsyncSession, user: models.User):
        return await db.execute(select(models.Order).filter(models.Order.user_id == user.id)).scalars().all()
    
    async def get_all_users(self, db: AsyncSession):
        result = await db.execute(select(models.User))
        return result.scalars().all()
    
    async def create_user(self, db: AsyncSession, user: models.User):
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        await db.refresh(user)
        return user
    
    async def delete_user(self, db: AsyncSession, user: models.User) -> None:
        await db.delete(user)
        await db.commit()

    async def update_user(self, db: AsyncSession, user: models.User):
        await db.commit()
        await db.refresh(user)
        return user
    
users = UserCrud()
