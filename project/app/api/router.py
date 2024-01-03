from fastapi import APIRouter, Depends

from app.api import ping, tools, videos, users
from app.auth.jwt import JWTManager

api_app = APIRouter()
api_app.include_router(ping.router)
api_app.include_router(tools.router, prefix="/tools", tags=["tools"])
api_app.include_router(videos.router, prefix="/videos", tags=["videos"])
api_app.include_router(users.router, prefix="/users", tags=["users"])

jwtmanager = JWTManager()


@api_app.get("/")
def test():
    return {"message": "unprotected api_app endpoint"}


@api_app.get("/protected")
def test2(current_email: str = Depends(jwtmanager.get_current_user_email)):
    return {"message": "protected api_app endpoint"}
