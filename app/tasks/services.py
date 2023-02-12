from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.tasks.dao import add_task, delete_task, get_task_ordering, get_tasks, tasks_ordering_change, update_task
from app.tasks.schemas import TaskCreateSchema, TaskOrdering, TaskResponse, TaskSchemaResponse, TaskUpdateSchema
from db.db import get_db


def get_tasks_service(list_id: int, board_id: int, user_id: int, db: Session) -> list:
    rows = get_tasks(list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    return [TaskSchemaResponse(**_) for _ in rows]


def create_task_services(
    task_: TaskCreateSchema, list_id: int, board_id: int, user_id: int, db: Session
) -> TaskResponse:
    ordering = get_task_ordering(list_id=list_id, board_id=board_id, db=db)
    task = add_task(**task_.dict(), ordering=ordering, list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    if task is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Performing an operation on someone else's board",
        )
    else:
        return TaskResponse(task_id=task.id, name=task.name, description=task.description, list_id=task.list_id)


def update_task_services(
    task_: TaskUpdateSchema, task_id: int, list_id: int, board_id: int, user_id: int, db: Session
) -> None:
    task = update_task(**task_.dict(), task_id=task_id, list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    if task is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Performing an operation on someone else's board",
        )
    else:
        return task


def delete_task_services(task_id: int, list_id: int, board_id: int, user_id: int, db: Session) -> None:
    task = delete_task(task_id=task_id, list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    if task is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Performing an operation on someone else's board",
        )
    else:
        return task


def tasks_ordering_services(
    ordering: TaskOrdering, task_id: int, list_id: int, board_id: int, user_id: int, db: Session = Depends(get_db)
) -> None:
    orderings = tasks_ordering_change(
        prev_task_ordering=ordering.prev_task_ordering,
        new_list_id=ordering.new_list_id,
        task_id=task_id,
        list_id=list_id,
        board_id=board_id,
        user_id=user_id,
        db=db,
    )
    if orderings is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Performing an operation on someone else's board",
        )
    else:
        return orderings
