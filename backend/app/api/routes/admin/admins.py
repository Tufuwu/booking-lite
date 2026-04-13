from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_admin
from app import schemas
from app.db import get_db
from app import services

router = APIRouter(
    prefix="/admins",
    tags=["admins"],
    dependencies=[Depends(get_current_admin)],
)


@router.post(
    "/",
    response_model=schemas.AdminOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return await services.create_admin(db, admin)


@router.post("/logout", status_code=204)
async def admin_logout(request: Request):
    return await services.checkout_admin(request)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_admin_me(
    request: Request,
    admin: schemas.AdminDelete,
    db: Session = Depends(get_db),
    current_admin: schemas.AdminOut = Depends(get_current_admin),
):
    return await services.delete_admin(request, db, admin, current_admin)

@router.patch(
    "/update",
    response_model=schemas.AdminOut,
    status_code=status.HTTP_200_OK
)
async def update_admin_me(
    admin: schemas.AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: schemas.AdminOut = Depends(get_current_admin),
):
    return await services.update_admin(db, admin, current_admin)


@router.get("/me")
async def get_current_user(current_admin: schemas.AdminOut = Depends(get_current_admin), db: Session = Depends(get_db)):

    user = await services.SessionService().get_user(db, current_admin)

    if not user:
        raise HTTPException(401)

    return user