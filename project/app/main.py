import logging
import os

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from app.api.router import api_app
from app.auth.jwt import CREDENTIALS_EXCEPTION, JWTManager
from app.auth.jwt_helper import add_blacklist_token, init_blacklist_file
from app.auth.router import auth_app
from app.db import init_db

# config
log = logging.getLogger("uvicorn")

SECRET_KEY = os.environ.get("SECRET_KEY") or None
if SECRET_KEY is None:
    raise "Missing SECRET_KEY"

ALLOWED_HOSTS = ["*"]


# JWT Manager
jwtmanager = JWTManager()


def create_application() -> FastAPI:
    # jwt blacklist
    init_blacklist_file()

    application = FastAPI()

    # Auth routes
    application.include_router(auth_app, prefix="/auth", tags=["auth"])
    application.include_router(api_app, prefix="/api", tags=["api"])

    # Configure middleware
    application.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")


@app.get("/")
async def root():
    return HTMLResponse('<body><a href="/auth/login">Log In</a></body>')


@app.get("/logout")
def logout(token: str = Depends(jwtmanager.get_current_user_token)):
    if add_blacklist_token(token):
        return JSONResponse({"result": True})
    raise CREDENTIALS_EXCEPTION
