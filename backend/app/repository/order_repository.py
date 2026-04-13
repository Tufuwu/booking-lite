from sqlalchemy.orm import Session

from app.db import models

class OrderRepository:
    async def get_by_id(self, db: Session, order_id: int):
        return db.query(models.Order).filter(models.Order.id == order_id).first()
    
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
        return db.query(models.Order).filter(*criterion).all()
    
orders = OrderRepository()