import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload  # 或 payload["sub"]
    except (ExpiredSignatureError, InvalidTokenError):
        return None


    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return user