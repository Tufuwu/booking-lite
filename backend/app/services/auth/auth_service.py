from .session_service import SessionService
from .jwt_service import JWTService

class AuthService:
    async def login_web(self, user, response):
        return await SessionService().create_session(user, response)

    def login_mobile(self, user):
        return JWTService().create_token(user)

    async def authenticate(self, request):
        # 混合认证入口
        # 1. session
        # 2. jwt
        pass