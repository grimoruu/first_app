from fastapi import HTTPException, status, Depends, APIRouter
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.user_util.jwt_utils import verify_password, create_access_token, create_refresh_token
from db.db import get_db
from db.models import User
from app.users.schemas import LoginUserSchema

router = APIRouter()


@router.post('')
def login(payload: LoginUserSchema, db: Session = Depends(get_db)):
    # Check if the user exist
    user = db.query(User).filter(
        User.email == EmailStr(payload.email.lower())).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email')

    # Check if the password is valid
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Password')

    # Create access token
    access_token = create_access_token(payload.email)

    # Create refresh token
    refresh_token = create_refresh_token(payload.email)
    # Send both access
    return {'status': 'success', 'access_token': access_token, 'refresh_token': refresh_token}
