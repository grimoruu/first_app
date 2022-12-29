from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.tasks.schemas import TaskSchema
from app.tasks.services import get_tasks_service
from db.db import get_db

router = APIRouter()


@router.get("", response_model=list[TaskSchema])
def get_all_tasks_api(db: Session = Depends(get_db)) -> list[TaskSchema]:
    return get_tasks_service(db=db)
