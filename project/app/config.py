import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: str

    # oauth
    google_client_id: str
    google_client_secret: str
    frontend_redirect_uri: AnyUrl = "http://localhost:8004/token"
    secret_key: str

    # jwt
    api_secret_key: str
    api_algorithm: str = "HS256"
    api_access_token_expire_minutes: int = 15


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
