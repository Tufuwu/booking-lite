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