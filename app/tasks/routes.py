from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.tasks.schemas import TaskNameDescSchema, TaskResponse, TaskSchema
from app.tasks.services import create_task_services, get_tasks_service, update_task_services, delete_task_services
from core.auth_utils.auth import get_user_by_token
from db.db import get_db

router = APIRouter()


@router.get("/{board_id}/lists/{list_id}/tasks", response_model=list[TaskSchema])
def get_all_tasks_api(board_id: int,
                      list_id: int,
                      db: Session = Depends(get_db),
                      user_id: int = Depends(get_user_by_token)) -> list[TaskSchema]:
    return get_tasks_service(user_id=user_id, board_id=board_id, list_id=list_id, db=db)


@router.post("/{board_id}/lists/{list_id}/tasks/create",
             status_code=status.HTTP_201_CREATED,
             response_model=TaskResponse)
def create_task_api(board_id: int,
                    list_id: int,
                    task: TaskNameDescSchema,
                    db: Session = Depends(get_db),
                    user_id: int = Depends(get_user_by_token)) -> TaskResponse:
    return create_task_services(user_id=user_id, board_id=board_id, list_id=list_id, task=task, db=db)


@router.put("/{board_id}/lists/{list_id}/tasks/{task_id}/update",
            status_code=status.HTTP_200_OK,
            response_model=TaskResponse)
def update_task_api(board_id: int,
                    list_id: int,
                    task_id: int,
                    task: TaskNameDescSchema,
                    db: Session = Depends(get_db),
                    user_id: int = Depends(get_user_by_token)) -> TaskResponse:
    return update_task_services(user_id=user_id, board_id=board_id,
                                list_id=list_id, task_id=task_id, task=task, db=db)


@router.delete("/{board_id}/lists/{list_id}/tasks/{task_id}/delete",
               status_code=status.HTTP_200_OK,
               response_model=TaskResponse)
def delete_task_api(board_id: int,
                    list_id: int,
                    task_id: int,
                    db: Session = Depends(get_db),
                    user_id: int = Depends(get_user_by_token)) -> TaskResponse:
    return delete_task_services(user_id=user_id, board_id=board_id,
                                list_id=list_id, task_id=task_id, db=db)
