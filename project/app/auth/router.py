import os
from datetime import datetime

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from app.auth.jwt import (  # isort:skip
    CREDENTIALS_EXCEPTION,
    create_refresh_token,
    create_token,
    decode_token,
    valid_email_from_db,
)

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID") or None
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET") or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException("Missing env variables")


# Set up oauth
config_data = {
    "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


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
    redirect_uri = "http://localhost:8004/token"  # request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_app.get("/token")
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(e)
        raise CREDENTIALS_EXCEPTION

    user = access_token.get("userinfo")
    email = user.get("email")

    request.session["user"] = dict(user)

    if valid_email_from_db(email):
        return JSONResponse(
            {
                "result": True,
                "access_token": create_token(email),
                "refresh_token": create_refresh_token(email),
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
                payload = decode_token(token)
                # Check if token is not expired
                if datetime.utcfromtimestamp(payload.get("exp")) > datetime.utcnow():
                    email = payload.get("sub")
                    # Validate email
                    if valid_email_from_db(email):
                        # Create and return token
                        return JSONResponse(
                            {"result": True, "access_token": create_token(email)}
                        )
    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION


@auth_app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)

    return RedirectResponse(url="/")
