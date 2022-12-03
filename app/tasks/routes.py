from fastapi import APIRouter

from app.tasks.services import get_tasks_service

router = APIRouter()


@router.get('/tasks')
def tasks_list():
    return get_tasks_service()
