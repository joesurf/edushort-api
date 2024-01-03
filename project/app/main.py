import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from app.api.router import api_app
from app.auth.jwt import CREDENTIALS_EXCEPTION, JWTManager
from app.auth.jwt_helper import add_blacklist_token, init_blacklist_file
from app.auth.router import auth_app
from app.config import get_settings
from app.db import init_db

# config
log = logging.getLogger("uvicorn")


ALLOWED_HOSTS = {
    "dev": ["*"],
    "prod": ["https://edushort.joesurf.io", "https://edushort-api.joesurf.io"],
}


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
    application.add_middleware(SessionMiddleware, secret_key=get_settings().secret_key)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS[get_settings().environment],
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


@app.get("/token")
async def token(request: Request):
    return HTMLResponse(
        """
                <script>
                function send(){
                    var req = new XMLHttpRequest();
                    req.onreadystatechange = function() {
                        if (req.readyState === 4) {
                            console.log(req.response);
                            if (req.response["result"] === true) {
                                window.localStorage.setItem('jwt', req.response["access_token"]);
                                window.localStorage.setItem('refresh', req.response["refresh_token"]);
                            }
                        }
                    }
                    req.withCredentials = true;
                    req.responseType = 'json';
                    req.open("get", "/auth/token?"+window.location.search.substr(1), true);
                    req.send("");
                }
                </script>
                <button onClick="send()">Get FastAPI JWT Token</button>
                <button onClick='fetch("http://localhost:8004/api/").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Unprotected API
                </button>
                <button onClick='fetch("http://localhost:8004/api/protected").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API without JWT
                </button>
                <button onClick='fetch("http://localhost:8004/api/protected",{
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                }).then((r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API wit JWT
                </button>
                <button onClick='fetch("http://localhost:8004/logout",{
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                }).then((r)=>r.json()).then((msg)=>{
                    console.log(msg);
                    if (msg["result"] === true) {
                        window.localStorage.removeItem("jwt");
                    }
                    });'>
                Logout
                </button>
                <button onClick='fetch("http://localhost:8004/auth/refresh",{
                    method: "POST",
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                    body:JSON.stringify({
                        grant_type:\"refresh_token\",
                        refresh_token:window.localStorage.getItem(\"refresh\")
                        })
                }).then((r)=>r.json()).then((msg)=>{
                    console.log(msg);
                    if (msg["result"] === true) {
                        window.localStorage.setItem("jwt", msg["access_token"]);
                    }
                    });'>
                Refresh
                </button>
            """
    )


@app.get("/logout")
def logout(token: str = Depends(jwtmanager.get_current_user_token)):
    if add_blacklist_token(token):
        return JSONResponse({"result": True})
    raise CREDENTIALS_EXCEPTION
