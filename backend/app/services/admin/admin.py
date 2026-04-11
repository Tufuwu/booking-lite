from app.repository.admin_repository import admin
import models
from sqlalchemy.orm import Session
import core

def login(db: Session, username: str, password: str):
    # 验证用户逻辑
    admin: models.Admin = admin.get_by_user_id(db, username)
    is_vaild_admin = core.security.verify_password(password, admin.password)
    if not is_vaild_admin:
        return None
    return "admin"