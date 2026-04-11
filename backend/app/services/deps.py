from fastapi import Request, HTTPException
from app.services.auth.auth_service import AuthService

auth_service = AuthService()

async def get_current_user(request: Request):
    user = await auth_service.authenticate(request)

    if not user:
        raise HTTPException(401, "Unauthorized")

    return user