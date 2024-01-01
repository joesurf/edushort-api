from fastapi import APIRouter, Depends

from app.api import ping, tools
from app.auth.jwt import get_current_user_email


api_app = APIRouter()
api_app.include_router(ping.router)
api_app.include_router(tools.router, prefix="/tools", tags=["tools"])

@api_app.get('/')
def test():
    return {'message': 'unprotected api_app endpoint'}


@api_app.get('/protected')
def test2(current_email: str = Depends(get_current_user_email)):
    return {'message': 'protected api_app endpoint'}