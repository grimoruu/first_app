from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.tasks.dao import add_new_task, get_task_ordering, get_tasks, update_task, delete_task
from app.tasks.schemas import TaskNameDescSchema, TaskResponse, TaskSchema


def get_tasks_service(user_id: int,
                      board_id: int,
                      list_id: int,
                      db: Session) -> list:
    rows = get_tasks(user_id=user_id, board_id=board_id,list_id=list_id, db=db)
    return [
        TaskSchema(
            **_
        )
        for _ in rows
    ]


def create_task_services(user_id: int, board_id: int, list_id: int,
                         task: TaskNameDescSchema, db: Session) -> TaskResponse:
    ordering = get_task_ordering(db=db)
    task_id = add_new_task(user_id, board_id, list_id, task.name, task.description, ordering, db)
    if task_id is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    return TaskResponse(task_id=task_id, name=task.name, description=task.description, list_id=list_id)


def update_task_services(user_id: int, board_id: int, list_id: int, task_id: int,
                         task: TaskNameDescSchema, db: Session) -> TaskResponse:
    task_id = update_task(user_id, board_id, list_id, task_id, task.name, task.description, db)
    if task_id is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    return TaskResponse(task_id=task_id, name=task.name, description=task.description, list_id=list_id)


def delete_task_services(user_id: int, board_id: int, list_id: int, task_id: int,
                         db: Session) -> TaskResponse:
    task = delete_task(user_id, board_id, list_id, task_id, db)
    if task is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    return TaskResponse(task_id=task_id, name=task[0], description=task[1], list_id=list_id)
