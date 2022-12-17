from fastapi import APIRouter

from app.tasks.schemas import TaskSchema
from app.tasks.services import get_tasks_service

router = APIRouter()


@router.get('/tasks', response_model=TaskSchema)
def tasks_list() -> list:
    return get_tasks_service()
