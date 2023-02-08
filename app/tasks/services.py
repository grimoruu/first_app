from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.tasks.dao import add_task, delete_task, get_task_ordering, get_tasks, update_task
from app.tasks.schemas import TaskResponse, TaskSchema, TasksGetSchema, TaskCreateSchema, TaskUpdateSchema, \
    TaskDeleteSchema


def get_tasks_service(task: TasksGetSchema, user_id: int, db: Session) -> list:
    rows = get_tasks(**task.dict(), user_id=user_id, db=db)
    return [TaskSchema(**row) for row in rows]


def create_task_services(task: TaskCreateSchema, user_id: int, db: Session) -> TaskResponse:
    ordering = get_task_ordering(list_id=task.list_id, board_id=task.board_id, db=db)
    task = add_task(**task.dict(), ordering=ordering, user_id=user_id, db=db)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Performing an operation on someone else's board",
        )
    return TaskResponse(task_id=task.id, name=task.name, description=task.description, list_id=task.list_id)


def update_task_services(task: TaskUpdateSchema, user_id: int, db: Session) -> TaskResponse:
    task = update_task(**task.dict(), user_id=user_id, db=db)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Performing an operation on someone else's board",
        )
    return TaskResponse(task_id=task.id, name=task.name, description=task.description, list_id=task.list_id)


def delete_task_services(task: TaskDeleteSchema, user_id: int, db: Session) -> TaskResponse:
    task = delete_task(**task.dict(), user_id=user_id, db=db)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Performing an operation on someone else's board",
        )
    return TaskResponse(task_id=task.id, name=task.name, description=task.description, list_id=task.list_id)
