from fastapi import APIRouter, Response, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from app.db import get_db
from app import services
router = APIRouter()

SESSION_EXPIRE = 7200  # 2小时

@router.post("/login")
async def admin_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):

    user = await services.login_user(db, form_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = services.auth.JWTService().create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

