from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app import schemas
from app.deps.auth import get_current_user
from app import services
from app.core.permissions import require_permission
router = APIRouter(
    prefix="/admins/room",
    tags=["admins"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/")
async def create_room(room: schemas.RoomCreate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("room:create"))):
    return await services.create_room(db, room)


@router.delete("/{room_number}")
async def delete_room(room_number: str, db: AsyncSession = Depends(get_db)):
    result = await services.delete_room(db, room_number)
    if not result:
        return {"detail": "Room not found"}
    return {"detail": "Room deleted successfully"}

@router.get("/all")
async def get_all_rooms(db: AsyncSession = Depends(get_db)):
    return await services.get_all_rooms(db)
