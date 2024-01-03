import logging
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt_helper import is_token_blacklisted
from app.auth.user_auth import valid_email_from_db
from app.config import get_settings

log = logging.getLogger("uvicorn")


# Token url (We should later create a token url that accepts just a user and a password to use it with Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class JWTManager:
    def __init__(self):
        self.API_SECRET_KEY = get_settings().api_secret_key
        self.API_ALGORITHM = get_settings().api_algorithm
        self.API_ACCESS_TOKEN_EXPIRE_MINUTES = (
            get_settings().api_access_token_expire_minutes
        )
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

    def _create_access_token(self, *, data: dict, expires_delta: timedelta = None):
        """Create token internal function"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.API_SECRET_KEY, algorithm=self.API_ALGORITHM
        )
        return encoded_jwt

    # Create token for an email
    def create_token(self, email):
        access_token_expires = timedelta(minutes=self.API_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )
        return access_token

    def create_refresh_token(self, email):
        expires = timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)
        return self._create_access_token(data={"sub": email}, expires_delta=expires)

    def decode_token(self, token):
        return jwt.decode(token, self.API_SECRET_KEY, algorithms=[self.API_ALGORITHM])

    def get_current_user_email(self, token: str = Depends(oauth2_scheme)):
        if is_token_blacklisted(token):
            log.warning("JWT Token blacklisted")
            raise CREDENTIALS_EXCEPTION

        try:
            payload = self.decode_token(token)
            email: str = payload.get("sub")
            if email is None:
                log.warning("Token decoding error")
                raise CREDENTIALS_EXCEPTION
        except jwt.PyJWTError as e:
            log.warning(f"JWT Error: {e}")
            raise CREDENTIALS_EXCEPTION

        if valid_email_from_db(email):
            return email

        log.warning(f"User email not found: {email}")
        raise CREDENTIALS_EXCEPTION

    async def get_current_user_token(self, token: str = Depends(oauth2_scheme)):
        _ = self.get_current_user_email(token)
        return token
