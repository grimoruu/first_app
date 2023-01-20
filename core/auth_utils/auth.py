from datetime import datetime, timedelta

import jwt
from argon2 import PasswordHasher, exceptions
from fastapi import Header, HTTPException, status

from app.auth.schemas import JWTResponse
from core.auth_utils.enum import ExpirationTime, ScopeAuthEnum, SecretKeys

ALGORITHM = "HS256"
ph = PasswordHasher()


def encode_password(password: str) -> str:
    """
    Hash password
    """
    return ph.hash(password)


def verify_password(password: str, encoded_password: str) -> bool:
    """
    Verify password with hash password
    """
    try:
        if ph.verify(encoded_password, password):
            return True
    except exceptions.VerifyMismatchError:
        return False


def create_token(
        user_id: int,
        expiration_time: timedelta = ExpirationTime,
        scope_auth: str = ScopeAuthEnum,
        secret_key: str = SecretKeys) -> str:
    """
    Create access or refresh token
    """
    payload = {
        'exp': datetime.utcnow() + expiration_time,
        'iat': datetime.utcnow(),
        'scope': scope_auth,
        'user_id': user_id
    }
    return jwt.encode(
        payload,
        secret_key,
        ALGORITHM
    )


def decode_token(
        token: str,
        scope_auth: str = ScopeAuthEnum,
        secret_key: str = SecretKeys) -> int:
    """
    Decode access token or refresh token
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        if payload['scope'] != scope_auth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Scope for the token is invalid')
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


def get_user_by_token(token: str = Header(..., alias="authorization")) -> int:
    if token.split()[0] != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not using the Bearer schema")
    return decode_access_token(token.split()[1])


def create_jwt_tokens(user_id: int) -> JWTResponse:
    access_token = create_token(
        user_id,
        ExpirationTime.ACCESS_TOKEN_EXPIRE_TIME.value,
        ScopeAuthEnum.ACCESS.value,
        SecretKeys.JWT_ACCESS_SECRET_KEY.value)
    refresh_token = create_token(
        user_id,
        ExpirationTime.REFRESH_TOKEN_EXPIRE_TIME.value,
        ScopeAuthEnum.REFRESH.value,
        SecretKeys.JWT_REFRESH_SECRET_KEY.value)
    return JWTResponse(access_token=access_token,
                       refresh_token=refresh_token)


def decode_access_token(token: str) -> int:
    return decode_token(token, ScopeAuthEnum.ACCESS.value, SecretKeys.JWT_ACCESS_SECRET_KEY.value)


def decode_refresh_token(token: str) -> int:
    return decode_token(token, ScopeAuthEnum.REFRESH.value, SecretKeys.JWT_REFRESH_SECRET_KEY.value)