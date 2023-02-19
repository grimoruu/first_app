from decimal import Decimal
from math import trunc

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.lists.dao import (
    add_list,
    check_true_users,
    delete_list,
    get_lists,
    get_lists_ordering,
    lists_ordering_change,
    select_lists_next_ordering,
    update_all_lists_ordering,
    update_list,
)
from app.lists.schemas import ListCreateSchema, ListSchemaResponse, ListUpdateSchema
from core.auth_utils.auth import get_user_by_token
from db.db import get_db


def get_lists_service(board_id: int, user_id: int, db: Session) -> list[ListSchemaResponse]:
    rows = get_lists(board_id=board_id, user_id=user_id, db=db)
    return [ListSchemaResponse(**_) for _ in rows]


def create_list_services(board_id: int, list_: ListCreateSchema, db: Session, check: bool) -> None:
    order = get_lists_ordering(board_id=board_id, db=db)
    ordering = trunc(order) + 1 if order else 1
    add_list(**list_.dict(), board_id=board_id, ordering=ordering, db=db)


def update_list_services(list_id: int, list_: ListUpdateSchema, db: Session, check: bool) -> None:
    update_list(list_id=list_id, **list_.dict(), db=db)


def delete_list_services(list_id: int, db: Session, check: bool) -> None:
    delete_list(list_id=list_id, db=db)


def lists_ordering_services(prev_list_ordering: float, list_id: int, board_id: int, db: Session, check: bool) -> None:
    next_ordering = select_lists_next_ordering(prev_list_ordering=prev_list_ordering, board_id=board_id, db=db)
    ordering = (next_ordering + prev_list_ordering) / 2 if next_ordering else prev_list_ordering / 2
    new_order = lists_ordering_change(list_id=list_id, ordering=ordering, db=db)
    if int(Decimal(str(new_order)).as_tuple().exponent * (-1)) > 5:
        update_all_lists_ordering(board_id=board_id, db=db)


def check_users_list_service(
    board_id: int = Path(title="board_id"), user_id: int = Depends(get_user_by_token), db: Session = Depends(get_db)
) -> bool:
    if user_id == check_true_users(board_id=board_id, db=db):
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Performing an operation on someone else's board",
        )
