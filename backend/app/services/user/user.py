from backend.app.schemas import admin
from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.db import get_db, models
from app import schemas
from app.repository import users
from app import core

async def login_user(db: Session, form_data):
    user: models.User = await users.get_by_user_phone_number(db, form_data.phone_number)
    if not user:
        return None
    is_vaild_user = core.security.verify_password(form_data.password, user.hashed_password)
    if not is_vaild_user:
        return None
    return {
        "id": user.id,
        "name": user.name,
        "role": "user",
    }
async def create_user(db: Session, user: schemas.UserCreate):

    is_user_exist: models.User = await users.get_by_user_name(db, user.name)
    if is_user_exist:
        return None
    hashed_password = core.security.hash_password(user.password)
    new_user = models.User(
        name=user.name,
        phone_number=user.phone_number,
        identity_number=user.identity_number,
        hashed_password=hashed_password,
        
    )
    return await users.create_user(db, new_user)

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