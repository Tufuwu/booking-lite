from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app import schemas
from app.deps.auth import get_current_user
from app import services

router = APIRouter(
    prefix="/admins/user",
    tags=["admins"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/all")
async def get_all_user(db: AsyncSession = Depends(get_db)):
    return await services.get_all_users(db)
