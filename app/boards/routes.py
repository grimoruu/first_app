from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.boards.schemas import BoardSchema
from app.boards.services import get_boards_service
from db.db import get_db

router = APIRouter()


@router.get("", response_model=list[BoardSchema])
def get_all_boards_api(db: Session = Depends(get_db)) -> list[BoardSchema]:
    return get_boards_service(db=db)
