from sqlalchemy.orm import Session

from app.db import models


class UserRepository:
    async def get_by_user_phone_number(self, db: Session, phone_number: str):
        return db.query(models.User).filter(models.User.phone_number == phone_number).first()

    async def get_by_user_name(self, db: Session, name: str):
        return db.query(models.User).filter(models.User.name == name).first()
    
    async def get_orders_by_user(self, db: Session, user: models.User):
        return db.query(models.Order).filter(models.Order.user_id == user.id).all()
    
    async def create_user(self, db: Session, user: models.User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    async def delete_user(self, db: Session, user: models.User) -> None:
        db.delete(user)
        db.commit()

    async def update_user(self, db: Session, user: models.User):
        db.commit()
        db.refresh(user)
        return user
users = UserRepository()