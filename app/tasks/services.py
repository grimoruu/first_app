from decimal import Decimal
from math import trunc

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.tasks.dao import (
    add_task,
    delete_task,
    get_task_ordering,
    get_tasks,
    select_tasks_next_ordering,
    tasks_ordering_update,
    update_all_task_ordering,
    update_task,
)
from app.tasks.schemas import TaskCreateSchema, TaskGetDataResponse, TaskOrderingSchema
from core.db_utils import get_paginated
from core.pagination.schemas import PaginationParams
from core.utils.number import get_count, number_length_check


def get_tasks_service(
    list_id: int | list, board_id: int, user_id: int, pagination: PaginationParams, *, db: Session
) -> TaskGetDataResponse:
    if isinstance(list_id, int):
        list_id = [list_id]
    query = get_tasks(list_id, board_id, user_id, pagination.limit, pagination.offset)
    items = get_paginated(query, None, None, db=db)
    total_count = get_count(items)
    return TaskGetDataResponse(total_count=total_count, offset=pagination.offset, limit=pagination.limit, items=items)


def create_task_services(task_create: TaskCreateSchema, list_id: int, *, db: Session) -> None:
    priority = get_task_ordering(list_id, db=db)
    ordering = Decimal(trunc(priority) + 1 if priority else 1)
    add_task(task_create.name, task_create.description, list_id, ordering, db=db)


def update_task_services(task_update: dict, task_id: int, *, db: Session) -> None:
    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="One of 'description' or 'name' needs to be set"
        )
    update_task(task_id, values=task_update, db=db)


def delete_task_services(task_id: int, *, db: Session) -> None:
    delete_task(task_id, db=db)


def tasks_ordering_services(task_ordering: TaskOrderingSchema, task_id: int, *, db: Session) -> None:
    if task_ordering.prev_task_ordering != 0:
        next_ordering = select_tasks_next_ordering(task_ordering.prev_task_ordering, task_ordering.new_list_id, db=db)
        ordering = (
            (next_ordering + task_ordering.prev_task_ordering) / 2
            if next_ordering
            else task_ordering.prev_task_ordering / 2
        )
    else:
        ordering = Decimal(1)
    tasks_ordering_update(task_id, ordering, task_ordering.new_list_id, db=db)
    if number_length_check(ordering):
        update_all_task_ordering(task_ordering.new_list_id, db=db)
