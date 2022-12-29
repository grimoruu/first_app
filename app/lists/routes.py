from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.lists.schemas import ListSchema
from app.lists.services import get_lists_service
from db.db import get_db

router = APIRouter()


@router.get("", response_model=list[ListSchema])
def get_all_lists_api(db: Session = Depends(get_db)) -> list[ListSchema]:
    return get_lists_service(db=db)
