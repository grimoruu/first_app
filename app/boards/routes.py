from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.boards.schemas import BoardSchema
from app.boards.services import get_boards_service
from core.auth_utils.auth import get_user_by_token
from db.db import get_db

router = APIRouter()


@router.get("", response_model=list[BoardSchema])
def get_all_boards_api(db: Session = Depends(get_db), user_id: int = Depends(get_user_by_token)) -> list[BoardSchema]:
    return get_boards_service(db=db)
