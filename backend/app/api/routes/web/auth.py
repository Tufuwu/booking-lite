from fastapi import APIRouter, Response, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from app.db import get_db
from app import services, schemas
router = APIRouter(prefix="/user",tags=["users"],)

SESSION_EXPIRE = 7200  # 2小时

@router.post(
    "/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return await services.create_user(db, user  )

@router.post("/login")
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, db: Annotated[Session, Depends(get_db)]):
    user = await services.login_user(db, form_data)
    if not user or user["role"] != "user":
        raise HTTPException(status_code=401, detail="Invalid user credentials")
    
    session_id = await services.auth.SessionService().create_session(user)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=7200,
        path="/"
    )
    return {"msg": "login success"}
