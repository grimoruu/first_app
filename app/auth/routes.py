from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.schemas import CreateUserSchema, JWTResponse, LoginUserSchema, RefreshTokenSchema
from app.auth.services import create_user_services, login_user_services, refresh_access_token_services
from db.db import get_db

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=JWTResponse)
def signup_user(payload: CreateUserSchema, db: Session = Depends(get_db)) -> JWTResponse:
    return create_user_services(payload=payload, db=db)


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=JWTResponse)
def login_user(payload: LoginUserSchema, db: Session = Depends(get_db)) -> JWTResponse:
    return login_user_services(payload=payload, db=db)


@router.post("/refresh", status_code=status.HTTP_202_ACCEPTED, response_model=JWTResponse)
def refresh_access_token(payload: RefreshTokenSchema) -> JWTResponse:
    return refresh_access_token_services(payload=payload)
