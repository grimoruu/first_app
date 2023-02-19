from decimal import Decimal
from math import trunc

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.tasks.dao import (
    add_task,
    check_true_users,
    delete_task,
    get_task_ordering,
    get_tasks,
    select_tasks_next_ordering,
    tasks_ordering_change,
    update_all_task_ordering,
    update_task,
)
from app.tasks.schemas import TaskCreateSchema, TaskOrdering, TaskSchemaResponse, TaskUpdateSchema
from core.auth_utils.auth import get_user_by_token
from db.db import get_db


def get_tasks_service(list_id: int, board_id: int, user_id: int, db: Session) -> list:
    rows = get_tasks(list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    return [TaskSchemaResponse(**_) for _ in rows]


def create_task_services(task_: TaskCreateSchema, list_id: int, db: Session, check: bool) -> None:
    order = get_task_ordering(list_id=list_id, db=db)
    ordering = trunc(order) + 1 if order else 1
    add_task(**task_.dict(), ordering=ordering, list_id=list_id, db=db)


def update_task_services(task_: TaskUpdateSchema, task_id: int, db: Session, check: bool) -> None:
    update_task(**task_.dict(), task_id=task_id, db=db)


def delete_task_services(task_id: int, db: Session, check: bool) -> None:
    delete_task(task_id=task_id, db=db)


def tasks_ordering_services(order: TaskOrdering, task_id: int, db: Session, check: bool) -> None:
    if order.prev_task_ordering != 0:
        next_ordering = select_tasks_next_ordering(
            prev_task_ordering=order.prev_task_ordering, new_list_id=order.new_list_id, db=db
        )
        ordering = (next_ordering + order.prev_task_ordering) / 2 if next_ordering else order.prev_task_ordering / 2
    else:
        ordering = 1
    new_order = tasks_ordering_change(task_id=task_id, ordering=ordering, new_list_id=order.new_list_id, db=db)
    if int(Decimal(str(new_order)).as_tuple().exponent * (-1)) > 5:
        update_all_task_ordering(list_id=order.new_list_id, db=db)


def check_users_task_service(
    list_id: int = Path(title="lists_id"),
    board_id: int = Path(title="board_id"),
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> bool:
    if user_id == check_true_users(list_id=list_id, board_id=board_id, db=db):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Performing an operation on someone else's board",
        )
