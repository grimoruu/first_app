from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.tasks.dao import add_task, delete_task, get_task_ordering, get_tasks, update_task
from app.tasks.schemas import TaskResponse, TaskSchema


def get_tasks_service(list_id: int, board_id: int, user_id: int, db: Session) -> list:
    rows = get_tasks(list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    return [
        TaskSchema(
            **_
        )
        for _ in rows
    ]


def create_task_services(name: str, description: str, list_id: int, board_id: int,
                         user_id: int, db: Session) -> TaskResponse:
    ordering = get_task_ordering(list_id=list_id, board_id=board_id, db=db)
    task = add_task(name=name, description=description, list_id=list_id, ordering=ordering,
                    board_id=board_id, user_id=user_id, db=db)
    if task is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    return TaskResponse(task_id=task[0], name=task[1], description=task[2], list_id=task[3])


def update_task_services(task_id: int, name: str, description: str, list_id: int, board_id: int,
                         user_id: int, db: Session) -> TaskResponse:
    task = update_task(task_id=task_id, name=name, description=description, list_id=list_id,
                       board_id=board_id, user_id=user_id, db=db)
    if task is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    return TaskResponse(task_id=task[0], name=task[1], description=task[2], list_id=task[3])


def delete_task_services(task_id: int, list_id: int, board_id: int,
                         user_id: int, db: Session) -> TaskResponse:
    task = delete_task(task_id=task_id, list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    if task is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    return TaskResponse(task_id=task[0], name=task[1], description=task[2], list_id=task[3])
