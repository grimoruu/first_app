from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from core.user_util.settings import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, ALGORITHM, \
    REFRESH_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_SECRET_KEY

hasher = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def encode_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(password: str, encoded_password: str) -> bool:
    return hasher.verify(password, encoded_password)


def create_access_token(email: str) -> str:
    payload = {
            'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': email
        }
    return jwt.encode(
            payload,
            JWT_SECRET_KEY,
            ALGORITHM
    )


def create_refresh_token(email) -> str:
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.utcnow(),
        'scope': 'refresh_token',
        'sub': email
    }
    return jwt.encode(
        payload,
        JWT_REFRESH_SECRET_KEY,
        ALGORITHM
    )


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if payload['scope'] == 'access_token':
            return payload['sub']
        raise HTTPException(status_code=401, detail='Scope for the token is invalid')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        if payload['scope'] == 'refresh_token':
            username = payload['sub']
            new_token = create_access_token(username)
            return new_token
        raise HTTPException(status_code=401, detail='Invalid scope for token')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token is expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
