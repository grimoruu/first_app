from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dao import add_new_user, check_users_exist, login_user
from app.auth.schemas import CreateUserSchema, JWTResponse, LoginUserSchema, RefreshTokenSchema
from core.auth_utils.auth import create_jwt_tokens, decode_refresh_token, encode_password, verify_password
from db.db import get_db


def create_user_services(payload: CreateUserSchema, db: Session = Depends(get_db)) -> JWTResponse:
    """
    Create user
    """
    # Check if user already exist
    if check_users_exist(payload.email, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account already exist")
    # Hash the password
    else:
        hashed_password = encode_password(payload.password)
        user_id = add_new_user(payload.username, hashed_password, payload.email, db)
        tokens = create_jwt_tokens(user_id)
        return JWTResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)


def login_user_services(payload: LoginUserSchema, db: Session = Depends(get_db)) -> JWTResponse:
    """
    Login user
    """
    user = login_user(payload.email, db)
    # Check if the user exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account dont exist or Incorrect Email",
        )
    # Check if the password is valid
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
    tokens = create_jwt_tokens(user.id)
    return JWTResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)


def refresh_access_token_services(payload: RefreshTokenSchema) -> JWTResponse:
    """
    Refresh access token
    """
    tokens = create_jwt_tokens(decode_refresh_token(payload.refresh_token))
    return JWTResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)
