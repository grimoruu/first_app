from fastapi import Depends, APIRouter, Security
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.users.schemas import CreateUserSchema

from core.user_util.jwt_utils import decode_access_token
from db.db import get_db
from db.models import User

security = HTTPBearer()

router = APIRouter()


def create_user(db: Session, user: CreateUserSchema):
    db_user = User(username=user.username, password=user.password, email=user.email)
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# @router.post('')
# def auth_user(
#         user: User,
#         db: Session = Depends(get_db()),
#         credentials: HTTPAuthorizationCredentials = Security(security)):
#     token = credentials.credentials
#     if decode_access_token(token):
#         return create_user(db=db, user=user)
#     return 'Invalid token'
