from .session_service import SessionService
from .jwt_service import JWTService

class AuthService:
    async def login_web(self, user, response):
        return await SessionService().create_session(user, response)

    def login_mobile(self, user):
        return JWTService().create_token(user)

    async def authenticate(self, request):
        # 1. 优先尝试 session（Web）
        session_id = request.cookies.get("session_id")
        if session_id:
            user = await SessionService().get_user(session_id)
            if user:
                return user

        # 2. 再尝试 JWT（Mobile / API）
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user = JWTService().verify_token(token)
            if user:
                return user

        # 3. 都失败
        raise UnauthorizedException()