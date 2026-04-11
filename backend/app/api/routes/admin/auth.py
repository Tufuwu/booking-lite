from fastapi import APIRouter, Response, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from app.db import get_db
import services
router = APIRouter(prefix="/admin")
router = APIRouter()

SESSION_EXPIRE = 7200  # 2小时

@router.post("/login")
async def admin_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, db: Annotated[Session, Depends(get_db)]):
    user = services.login(db, form_data.username, form_data.password)
    if not user or user["type"] != "admin":
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    session_id = await services.auth.SessionService().create_session(user)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,        
        samesite="None",    
        max_age=7200,
        path="/"
    )
    return {"msg": "login success"}