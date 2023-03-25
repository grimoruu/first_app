from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.lists.depends import check_users_list_service
from app.tasks.depends import check_users_task_service
from app.tasks.schemas import TaskCreateSchema, TaskGetDataResponse, TaskOrderingSchema, TaskUpdateSchema
from app.tasks.services import (
    create_task_services,
    delete_task_services,
    get_tasks_service,
    tasks_ordering_services,
    update_task_services,
)
from app.users.depends import get_user_by_token
from core.pagination.schemas import PaginationParams
from db.db import get_read_db, get_write_db

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=TaskGetDataResponse)
def get_tasks_api(
    list_id: int,
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_read_db),
) -> TaskGetDataResponse:
    return get_tasks_service(list_id, board_id, user_id, pagination, db=db)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task_api(
    task_create: TaskCreateSchema,
    list_id: int,
    db: Session = Depends(get_write_db),
    _: None = Depends(check_users_list_service),
) -> None:
    create_task_services(task_create, list_id, db=db)


@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
def update_task_api(
    task_update: TaskUpdateSchema,
    task_id: int,
    db: Session = Depends(get_write_db),
    _: None = Depends(check_users_task_service),
) -> TaskUpdateSchema:
    update_task_services(task_update.dict(exclude_unset=True), task_id, db=db)
    return task_update


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_api(
    task_id: int,
    db: Session = Depends(get_write_db),
    _: None = Depends(check_users_task_service),
) -> None:
    delete_task_services(task_id, db=db)


@router.post("/{task_id}/ordering", status_code=status.HTTP_200_OK)
def ordering_list_api(
    task_ordering: TaskOrderingSchema,
    task_id: int,
    db: Session = Depends(get_write_db),
    _: None = Depends(check_users_task_service),
) -> None:
    tasks_ordering_services(task_ordering, task_id, db=db)
