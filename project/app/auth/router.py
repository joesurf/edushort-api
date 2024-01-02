import logging
from datetime import datetime

from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from app.auth.jwt import CREDENTIALS_EXCEPTION, JWTManager
from app.auth.oauth import oauth
from app.auth.user_auth import valid_email_from_db

log = logging.getLogger("uvicorn")

jwtmanager = JWTManager()

auth_app = APIRouter()


@auth_app.get("/")
def public(request: Request):
    user = request.session.get("user")
    if user:
        name = user.get("name")
        return HTMLResponse(f"<p>Hello {name}!</p><a href=/logout>Logout</a>")
    return HTMLResponse("<a href=/login>Login</a>")


@auth_app.get("/login")
async def login(request: Request):
    redirect_uri = "https://edushort-api.joesurf.io/auth/token"  # request.url_for("auth")
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_app.get("/token")
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        log.warning(f"OAuth Error: {e}")
        raise CREDENTIALS_EXCEPTION

    user = access_token.get("userinfo")
    email = user.get("email")

    request.session["user"] = dict(user)

    if valid_email_from_db(email):
        return JSONResponse(
            {
                "result": True,
                "access_token": jwtmanager.create_token(email),
                "refresh_token": jwtmanager.create_refresh_token(email),
            }
        )

    raise CREDENTIALS_EXCEPTION


@auth_app.post("/refresh")
async def refresh(request: Request):
    try:
        # Only accept post requests
        if request.method == "POST":
            form = await request.json()
            if form.get("grant_type") == "refresh_token":
                token = form.get("refresh_token")
                payload = jwtmanager.decode_token(token)
                # Check if token is not expired
                if datetime.utcfromtimestamp(payload.get("exp")) > datetime.utcnow():
                    email = payload.get("sub")
                    # Validate email
                    if valid_email_from_db(email):
                        # Create and return token
                        return JSONResponse(
                            {
                                "result": True,
                                "access_token": jwtmanager.create_token(email),
                            }
                        )
    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION


@auth_app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)

    return RedirectResponse(url="/")
