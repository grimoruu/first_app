from decimal import Decimal
from math import trunc

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.lists.dao import (
    add_list,
    delete_list,
    get_lists,
    get_lists_ordering,
    lists_ordering_update,
    select_lists_next_ordering,
    update_board_lists_ordering,
    update_list,
)
from app.lists.schemas import ListCreateSchema, ListGetDataResponse
from core.db_utils import get_count_of_queries, get_paginated
from core.pagination.schemas import PaginationParams
from core.utils.number import number_length_check


def get_lists_service(board_id: int, user_id: int, pagination: PaginationParams, *, db: Session) -> ListGetDataResponse:
    query = get_lists(board_id, user_id)
    total_count = get_count_of_queries(query, db=db)
    items = get_paginated(query, pagination.limit, pagination.offset, db=db)
    return ListGetDataResponse(total_count=total_count, offset=pagination.offset, limit=pagination.limit, items=items)


def create_list_services(board_id: int, *, list_create: ListCreateSchema, db: Session) -> None:
    priority = get_lists_ordering(board_id, db=db)
    ordering = Decimal(trunc(priority) + 1 if priority else 1)
    add_list(list_create.name, list_create.description, board_id, ordering, db=db)


def update_list_services(list_id: int, *, list_update: dict, db: Session) -> None:
    if not list_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="One of 'description' or 'name' needs to be set"
        )
    update_list(list_id, values=list_update, db=db)


def delete_list_services(list_id: int, *, db: Session) -> None:
    delete_list(list_id, db=db)


def lists_ordering_services(prev_list_ordering: Decimal, list_id: int, board_id: int, *, db: Session) -> None:
    next_ordering = select_lists_next_ordering(prev_list_ordering, board_id, db=db)
    ordering = (next_ordering + prev_list_ordering) / 2 if next_ordering else prev_list_ordering / 2
    lists_ordering_update(list_id, ordering, db=db)
    if number_length_check(ordering):
        update_board_lists_ordering(board_id, db=db)
