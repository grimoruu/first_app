from datetime import datetime

import jwt
from argon2 import PasswordHasher, exceptions
from fastapi import HTTPException, status

from app.auth.schemas import JWTResponse
from core.auth_utils.enum import ExpirationTime, ScopeAuthEnum, SecretKeys

ALGORITHM = "HS256"
ph = PasswordHasher()


def encode_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, encoded_password: str) -> bool:
    """
    Verify password with hash password
    """
    try:
        return ph.verify(encoded_password, password)
    except exceptions.VerifyMismatchError:
        return False


def create_token(
    user_id: int, *, expiration_time: ExpirationTime, scope_auth: ScopeAuthEnum, secret_key: SecretKeys
) -> str:
    """
    Create access or refresh token
    """
    payload = {
        "exp": datetime.utcnow() + expiration_time.value,
        "iat": datetime.utcnow(),
        "scope": scope_auth,
        "user_id": user_id,
    }
    return jwt.encode(payload, secret_key, ALGORITHM)


def decode_token(token: str, *, scope_auth: ScopeAuthEnum, secret_key: SecretKeys) -> int:
    """
    Decode access token or refresh token
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        if payload["scope"] != scope_auth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Scope for the token is invalid",
            )
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def create_jwt_tokens(user_id: int) -> JWTResponse:
    access_token = create_token(
        user_id,
        expiration_time=ExpirationTime.ACCESS_TOKEN_EXPIRE_TIME,
        scope_auth=ScopeAuthEnum.ACCESS,
        secret_key=SecretKeys.JWT_ACCESS_SECRET_KEY,
    )
    refresh_token = create_token(
        user_id,
        expiration_time=ExpirationTime.REFRESH_TOKEN_EXPIRE_TIME,
        scope_auth=ScopeAuthEnum.REFRESH,
        secret_key=SecretKeys.JWT_REFRESH_SECRET_KEY,
    )
    return JWTResponse(access_token=access_token, refresh_token=refresh_token)


def decode_access_token(token: str) -> int:
    return decode_token(
        token=token,
        scope_auth=ScopeAuthEnum.ACCESS,
        secret_key=SecretKeys.JWT_ACCESS_SECRET_KEY,
    )


def decode_refresh_token(token: str) -> int:
    return decode_token(
        token=token,
        scope_auth=ScopeAuthEnum.REFRESH,
        secret_key=SecretKeys.JWT_REFRESH_SECRET_KEY,
    )
