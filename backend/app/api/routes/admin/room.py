from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas
from app.core.security import get_current_admin
from app import services

router = APIRouter(
    prefix="/admins/room",
    tags=["admins"],
    dependencies=[Depends(get_current_admin)],
)

@router.post("/")
async def create_admin(admin: schemas.RoomCreate, db: Session = Depends(get_db)):
    return await services.create_room(db, admin)


@router.delete("/{room_number}")
async def delete_admin(room_number: str, db: Session = Depends(get_db)):
    result = await services.delete_room(db, room_number)
    if not result:
        return {"detail": "Room not found"}
    return {"detail": "Room deleted successfully"}

@router.get("/all")
async def get_all_rooms(db: Session = Depends(get_db)):
    return await services.get_all_rooms(db)