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
        user = payload
    except ExpiredSignatureError:
        raise HTTPException(401, "Token 已过期")
    except InvalidTokenError:
        raise HTTPException(401, "Token 无效")

    if user is None:
        raise HTTPException(401, "未认证")

    return user