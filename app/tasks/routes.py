from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.tasks.schemas import TaskCreateSchema, TaskOrdering, TaskSchemaResponse, TaskUpdateSchema
from app.tasks.services import (
    check_users_task_service,
    create_task_services,
    delete_task_services,
    get_tasks_service,
    tasks_ordering_services,
    update_task_services,
)
from core.auth_utils.auth import get_user_by_token
from db.db import get_db

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=list[TaskSchemaResponse])
def get_all_tasks_api(
    list_id: int,
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> list[TaskSchemaResponse]:
    return get_tasks_service(list_id=list_id, board_id=board_id, user_id=user_id, db=db)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task_api(
    task: TaskCreateSchema,
    list_id: int,
    db: Session = Depends(get_db),
    check: bool = Depends(check_users_task_service),
) -> None:
    create_task_services(task_=task, list_id=list_id, db=db, check=check)


@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
def update_task_api(
    task: TaskUpdateSchema,
    task_id: int,
    db: Session = Depends(get_db),
    check: bool = Depends(check_users_task_service),
) -> None:
    update_task_services(task_=task, task_id=task_id, db=db, check=check)


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_api(
    task_id: int,
    db: Session = Depends(get_db),
    check: bool = Depends(check_users_task_service),
) -> None:
    delete_task_services(task_id=task_id, db=db, check=check)


@router.post("/{task_id}/order", status_code=status.HTTP_200_OK)
def ordering_list_api(
    order: TaskOrdering,
    task_id: int,
    db: Session = Depends(get_db),
    check: bool = Depends(check_users_task_service),
) -> None:
    tasks_ordering_services(order=order, task_id=task_id, db=db, check=check)
