import services
import schemas
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_db

router = APIRouter(prefix="/admin")
@router.post("/login")
async def login( form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return services.login(db, form_data.username, form_data.password)

@router.post(
    "/",
    response_model=schemas.AdminOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return await services.create_admin(db, admin)