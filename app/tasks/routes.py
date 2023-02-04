from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.tasks.schemas import (
    TaskCreateSchema,
    TaskDeleteSchema,
    TaskResponse,
    TaskSchema,
    TasksGetSchema,
    TaskUpdateSchema,
)
from app.tasks.services import create_task_services, delete_task_services, get_tasks_service, update_task_services
from core.auth_utils.auth import get_user_by_token
from db.db import get_db

router = APIRouter()


@router.get("", response_model=list[TaskSchema])
def get_all_tasks_api(task: TasksGetSchema,
                      user_id: int = Depends(get_user_by_token),
                      db: Session = Depends(get_db)) -> list[TaskSchema]:
    return get_tasks_service(list_id=task.list_id, board_id=task.board_id, user_id=user_id, db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task_api(task: TaskCreateSchema,
                    user_id: int = Depends(get_user_by_token),
                    db: Session = Depends(get_db)) -> TaskResponse:
    return create_task_services(name=task.name, description=task.description, list_id=task.list_id,
                                board_id=task.board_id, user_id=user_id, db=db)


@router.patch("", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def update_task_api(task: TaskUpdateSchema,
                    user_id: int = Depends(get_user_by_token),
                    db: Session = Depends(get_db)) -> TaskResponse:
    return update_task_services(task_id=task.task_id, name=task.name, description=task.description,
                                list_id=task.list_id, board_id=task.board_id, user_id=user_id, db=db)


@router.delete("", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def delete_task_api(task: TaskDeleteSchema,
                    user_id: int = Depends(get_user_by_token),
                    db: Session = Depends(get_db)) -> TaskResponse:
    return delete_task_services(task_id=task.task_id, list_id=task.list_id,
                                board_id=task.board_id, user_id=user_id, db=db)
