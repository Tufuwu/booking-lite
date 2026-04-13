from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session

from app import core
from app import schemas
from app.db import models
from app.repository.admin_repository import admins

from ..auth.session_service import SessionService


async def login_admin(db: Session, form_data):
    admin: models.Admin = await admins.get_by_user_name(db, form_data.username)
    if not admin:
        return None
    is_vaild_admin = core.security.verify_password(form_data.password, admin.hashed_password)
    if not is_vaild_admin:
        return None
    return {
        "job_number": admin.job_number,
        "name": admin.name,
        "role": "admin",
    }


async def create_admin(db: Session, admin: schemas.AdminCreate):
    is_admin_exist: models.Admin = await admins.get_by_user_name(db, admin.name)
    if is_admin_exist:
        return None
    hashed_password = core.security.hash_password(admin.password)
    new_admin = models.Admin(
        job_number=admin.job_number,
        name=admin.name,
        hashed_password=hashed_password,
    )
    return await admins.create_admin(db, new_admin)


async def checkout_admin(request: Request):
    session_id = request.cookies.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing session",
        )

    session_data = await SessionService().get_session(session_id)

    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
        )

    return await SessionService().delete_session(session_id)

async def update_admin(db: Session, admin: schemas.AdminUpdate, current_admin_id: dict):
    admin_in_db: models.Admin = await admins.get_by_job_number(db, current_admin_id["user_id"])
    if not admin_in_db:
        return None
    if admin.name:
        admin_in_db.name = admin.name
    if admin.password:
        hashed_password = core.security.hash_password(admin.password)
        admin_in_db.hashed_password = hashed_password
    return await admins.update_admin(db, admin_in_db)

async def delete_admin(
    request: Request,
    db: Session,
    delete_admin: schemas.AdminDelete,
    current_admin_name: dict,
):
    admin: models.Admin = await admins.get_by_job_number(db, current_admin_name["user_id"])
    if not admin:
        return None
    is_vaild_admin = core.security.verify_password(delete_admin.password, admin.hashed_password)
    if not is_vaild_admin:
        return None
    await checkout_admin(request)
    await admins.delete_admin(db, admin)
