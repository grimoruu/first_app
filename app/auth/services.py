from datetime import datetime, timedelta
from enum import Enum

import jwt
from argon2 import PasswordHasher, exceptions
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dao import add_new_user, check_users_exist, login_user
from app.auth.schemas import CreateUserSchema, LoginUserSchema, RefreshTokenSchema, Token
from db.db import get_db

ALGORITHM = "HS256"
router = APIRouter()
ph = PasswordHasher()


class ScopeAuthEnum(Enum):
    ACCESS: str = "access_token"
    REFRESH: str = "refresh_token"


class ExpirationTime(Enum):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10


class SecretKeys(Enum):
    JWT_ACCESS_SECRET_KEY: str = "JWT_ACCESS_SECRET_KEY"
    JWT_REFRESH_SECRET_KEY: str = "JWT_REFRESH_SECRET_KEY"


#  Hash password
def encode_password(password: str) -> str:
    return ph.hash(password)


#  Verify password with hash password
def verify_password(password: str, encoded_password: str) -> bool:
    try:
        if ph.verify(encoded_password, password):
            return True
    except exceptions.VerifyMismatchError:
        return False


# Create access or refresh token
def create_token(
        user_id: int,
        expiration_time: float = ExpirationTime,
        scope_auth: str = ScopeAuthEnum,
        secret_key: str = SecretKeys) -> str:
    payload = {
            'exp': datetime.utcnow() + timedelta(minutes=expiration_time),
            'iat': datetime.utcnow(),
            'scope': scope_auth,
            'user_id': user_id
        }
    return jwt.encode(
            payload,
            secret_key,
            ALGORITHM
    )


#  Decode access token or refresh token
def decode_token(
        token: str,
        scope_auth: str = ScopeAuthEnum,
        secret_key: str = SecretKeys) -> id:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        if payload['scope'] != scope_auth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Scope for the token is invalid')
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


def get_user_by_token(authorization: str = Header(...)) -> id:
    return decode_token(
        authorization,
        ScopeAuthEnum.ACCESS.value,
        SecretKeys.JWT_ACCESS_SECRET_KEY.value
    )


#  Create user
def create_user_services(payload: CreateUserSchema, db: Session = Depends(get_db)) -> Token:
    # Check if user already exist
    if check_users_exist(payload, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    # Hash the password
    else:
        payload.password = encode_password(payload.password)
        user = add_new_user(payload, db)
        # Create access token
        access_token = create_token(
            user.id,
            ExpirationTime.ACCESS_TOKEN_EXPIRE_MINUTES.value,
            ScopeAuthEnum.ACCESS.value,
            SecretKeys.JWT_ACCESS_SECRET_KEY.value)
        refresh_token = create_token(
            user.id,
            ExpirationTime.REFRESH_TOKEN_EXPIRE_MINUTES.value,
            ScopeAuthEnum.REFRESH.value,
            SecretKeys.JWT_REFRESH_SECRET_KEY.value)
        return Token(access_token=access_token,
                     refresh_token=refresh_token)


#  Login user
def login_user_services(payload: LoginUserSchema, db: Session = Depends(get_db)) -> Token:
    user = login_user(payload, db)
    # Check if the user exist
    if not check_users_exist(payload, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account dont exist or Incorrect Email')
    # Check if the password is valid
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Incorrect Password')
    # Create access token
    access_token = create_token(
        user.id,
        ExpirationTime.ACCESS_TOKEN_EXPIRE_MINUTES.value,
        ScopeAuthEnum.ACCESS.value,
        SecretKeys.JWT_ACCESS_SECRET_KEY.value)

    # Create refresh token
    refresh_token = create_token(
        user.id,
        ExpirationTime.REFRESH_TOKEN_EXPIRE_MINUTES.value,
        ScopeAuthEnum.REFRESH.value,
        SecretKeys.JWT_REFRESH_SECRET_KEY.value
    )
    # Send both access
    return Token(access_token=access_token,
                 refresh_token=refresh_token)


# Refresh access token
def refresh_access_token_services(payload: RefreshTokenSchema) -> Token:
    token = payload.refresh_token
    user_id = decode_token(
        token,
        ScopeAuthEnum.REFRESH.value,
        SecretKeys.JWT_REFRESH_SECRET_KEY.value)
    access_token = create_token(
        user_id,
        ExpirationTime.ACCESS_TOKEN_EXPIRE_MINUTES.value,
        ScopeAuthEnum.ACCESS.value,
        SecretKeys.JWT_ACCESS_SECRET_KEY.value)
    refresh_token = create_token(
        user_id,
        ExpirationTime.REFRESH_TOKEN_EXPIRE_MINUTES.value,
        ScopeAuthEnum.REFRESH.value,
        SecretKeys.JWT_REFRESH_SECRET_KEY.value)
    return Token(access_token=access_token,
                 refresh_token=refresh_token)
