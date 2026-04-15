from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class JWTService:

    def create_access_token(self, data: dict):
        to_encode = data.copy()

        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({
            "exp": expire,
            "iat": now,
            "type": "access"
        })

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str):
        try:
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
        except (ExpiredSignatureError, InvalidTokenError):
            return None