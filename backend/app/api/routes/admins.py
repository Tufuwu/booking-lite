from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth import get_current_user
from app import schemas
from app import core
from app.db import get_db
from app import services
from app.crud import users
from app.core.permissions import require_permission
router = APIRouter(
    tags=["admins"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/users")
async def create_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("user:create"))
):
    print(user.identity_number)
    return await services.create_user(db, user)


@router.post("/logout", status_code=204)
async def logout(request: Request):
    return await services.checkout(request)



@router.get("/users/me")
async def get_current_user_info(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    user = await services.get_me(db, current_user)

    if not user:
        raise HTTPException(401)

    return user


@router.delete("/admins/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_admin(
    payload: schemas.UserDelete,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    db_user = await users.get_by_user_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not core.security.verify_password(payload.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    await users.delete_user(db, db_user)

@router.get("/users/all")
async def get_all_user(db: AsyncSession = Depends(get_db)):
    return await services.get_all_users(db)
