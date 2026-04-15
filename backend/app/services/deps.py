from fastapi import Request, HTTPException
from app.services.auth.auth_service import AuthService

auth_service = AuthService()

async def get_current_user(request: Request):
    user = await auth_service.authenticate(request)

    if not user:
        raise HTTPException(401, "Unauthorized")

    return {
        "id": user.id,
        "name": user.name,
        "phone_number": user.phone_number,
        "identity_number": user.identity_number,
        "role_id": user.role_id,
        "role": {
            "id": user.role.id,
            "name": user.role.name,
        } if user.role else None,
        "permissions": [
            p.code for p in (user.role.permissions if user.role else [])
        ]
    }