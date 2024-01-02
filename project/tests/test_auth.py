import pytest

from fastapi import HTTPException


def test_jwt_api_token_encoding_and_decoding(test_jwt):
    email = "test@gmail.com"
    token = test_jwt.create_token(email)

    payload = test_jwt.decode_token(token)
    email_decoded: str = payload.get("sub")

    assert email == email_decoded


def test_jwt_refresh_token_encoding_and_decoding(test_jwt):
    email = "test@gmail.com"
    token = test_jwt.create_refresh_token(email)

    payload = test_jwt.decode_token(token)
    email_decoded: str = payload.get("sub")

    assert email == email_decoded


def test_token_invalid(test_jwt):
    email = "test@gmail.com"
    token = test_jwt.create_token(email)

    with pytest.raises(HTTPException) as err:
        test_jwt.get_current_user_email(token)
    assert err.value.status_code == 401
    assert err.value.detail == "Could not validate credentials"
    assert err.value.headers == {"WWW-Authenticate": "Bearer"}
    