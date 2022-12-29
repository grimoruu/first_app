from fastapi import HTTPException, status, Depends, APIRouter
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.user_util.jwt_utils import encode_password
from db.db import get_db
from db.models import User
from app.users.schemas import CreateUserSchema

router = APIRouter()


# Register a new user
@router.post('', status_code=status.HTTP_201_CREATED, response_model=CreateUserSchema)
def create_user(payload: CreateUserSchema, db: Session = Depends(get_db)):
    # Check if user already exist
    user = db.query(User).filter(
        User.email == EmailStr(payload.email.lower())).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    #  Hash the password
    try:
        payload.password = encode_password(payload.password)
        new_user = User(**payload.dict())
        # CreateUserSchema(username=new_user.username, password=new_user.password, email=new_user.email)
        db.add(new_user)
        db.commit()
        # db.refresh(new_user) #  ??
        return CreateUserSchema(username=new_user.username, password=new_user.password, email=new_user.email)
    except:  # требует finally
        error_msg = "Failed to signup"
        return error_msg
