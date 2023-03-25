from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dao import add_new_user, check_users_exist, login_user
from app.auth.schemas import CreateUserSchema, JWTResponse, LoginUserSchema, RefreshTokenSchema
from core.auth_utils.auth import (
    create_jwt_tokens,
    decode_refresh_token,
    encode_password,
    verify_password,
)
from db.db import get_read_db


def create_user_services(payload: CreateUserSchema, db: Session = Depends(get_read_db)) -> JWTResponse:
    # Check if user already exist
    if check_users_exist(email=payload.email, db=db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account already exist")
    else:
        hashed_password = encode_password(password=payload.password)
        user_id = add_new_user(username=payload.username, hashed_password=hashed_password, email=payload.email, db=db)
        tokens = create_jwt_tokens(user_id=user_id)
        return JWTResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)


def login_user_services(payload: LoginUserSchema, db: Session = Depends(get_read_db)) -> JWTResponse:
    user = login_user(email=payload.email, db=db)
    # Check if the user exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account dont exist or Incorrect Email",
        )
    if not verify_password(password=payload.password, encoded_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect Password")
    tokens = create_jwt_tokens(user_id=user.id)
    return JWTResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)


def refresh_access_token_services(payload: RefreshTokenSchema) -> JWTResponse:
    tokens = create_jwt_tokens(user_id=decode_refresh_token(token=payload.refresh_token))
    return JWTResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token)
