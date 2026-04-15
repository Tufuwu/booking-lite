from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session

from app.deps.auth import get_current_user
from app import schemas
from app.db import get_db
from app import services
from app.crud import users
from app.core.permissions import require_permission
router = APIRouter(
    prefix="/users",
    tags=["admins"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/users")
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("user:create"))
):
    return await services.create_user(db, user)


@router.post("/logout", status_code=204)
async def logout(request: Request):
    return await services.checkout(request)



@router.get("/me")
async def get_current_user(current_user = Depends(get_current_user), db: Session = Depends(get_db)):

    user = await services.get_me(db, current_user)

    if not user:
        raise HTTPException(401)

    return user