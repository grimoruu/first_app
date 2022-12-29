from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.users.schemas import UserSchema
from app.users.services import get_users_service
from db.db import get_db

router = APIRouter()


@router.get("", response_model=list[UserSchema])
def get_all_users_api(db: Session = Depends(get_db)) -> list[UserSchema]:
    return get_users_service(db=db)


