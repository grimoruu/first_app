from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.users.schemas import UserSchemaResponse
from app.users.services import get_users_service
from db.db import get_read_db

router = APIRouter()


@router.get("", response_model=UserSchemaResponse)
def get_all_users_api(db: Session = Depends(get_read_db)) -> UserSchemaResponse:
    return get_users_service(db=db)
