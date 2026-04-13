from sqlalchemy.orm import Session

from app.db import models

class RoomRepository:
    async def get_by_room_number(self, db: Session, room_number: str):
        return db.query(models.Room).filter(models.Room.room_number == room_number).first()
    
    async def create_room(self, db: Session, room: models.Room):
        db.add(room)
        db.commit()
        db.refresh(room)
        return room
    
    async def delete_room(self, db: Session, room: models.Room) -> None:
        db.delete(room)
        db.commit()

    async def update_room(self, db: Session, room: models.Room):
        db.commit()
        db.refresh(room)
        return room
    
    async def get_all_rooms(self, db: Session):
        return db.query(models.Room).all()
    
    async def get_order_by_room_number(self, db: Session, room_number: str):
        return db.query(models.Order).filter(models.Order.room_number == room_number).first()
    
rooms = RoomRepository()