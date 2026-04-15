from fastapi import Depends, HTTPException, status
from app.db.models import User
from app.deps.auth import get_current_user


def require_permission(permission_code: str):

    async def checker(current_user: User = Depends(get_current_user)):

        # 1. 获取用户角色权限
        role = current_user.role

        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role"
            )

        permissions = [p.code for p in role.permissions]

        # 2. 校验权限
        if permission_code not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {permission_code}"
            )

        return current_user

    return checker