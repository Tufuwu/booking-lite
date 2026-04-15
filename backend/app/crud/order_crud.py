from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import models

class OrderCrud:
    async def get_by_id(self, db: Session, order_id: int):
        result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
        return result.scalar_one_or_none()
 
    async def create_order(self, db: Session, order: models.Order):
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    
    async def delete_order(self, db: Session, order: models.Order) -> None:
        db.delete(order)
        db.commit()

    async def update_order(self, db: Session, order: models.Order):
        db.commit()
        db.refresh(order)
        return order

    async def get_by_criterion(self, db: Session, criterion: list):
        return await db.execute(select(models.Order).filter(*criterion)).scalars().all()

orders = OrderCrud()