from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.lists.dao import add_list, delete_list, get_lists, get_lists_ordering, swap_lists_ordering, update_list
from app.lists.schemas import (
    ListResponse,
    ListSchema,
    ListsGetSchema,
    ListCreateSchema,
    ListUpdateSchema,
    ListDeleteSchema,
    Ordering,
)
from db.db import get_db


def get_lists_service(list_: ListsGetSchema, user_id: int, db: Session = Depends(get_db)) -> list[ListSchema]:
    rows = get_lists(**list_.dict(), user_id=user_id, db=db)
    return [ListSchema(**row) for row in rows]


def create_list_services(list_: ListCreateSchema, user_id: int, db: Session = Depends(get_db)) -> ListResponse:
    ordering = get_lists_ordering(board_id=list_.board_id, db=db)
    list_ = add_list(**list_.dict(), ordering=ordering, user_id=user_id, db=db)
    if list_ is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Performing an operation on someone else's board",
        )
    else:
        return ListResponse(list_id=list_.id, name=list_.name, board_id=list_.board_id)


def update_list_services(list_: ListUpdateSchema, user_id: int, db: Session = Depends(get_db)) -> ListResponse:
    list_ = update_list(**list_.dict(), user_id=user_id, db=db)
    if list_ is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Performing an operation on someone else's board",
        )
    else:
        return ListResponse(list_id=list_.id, name=list_.name, board_id=list_.board_id)


def delete_list_services(list_: ListDeleteSchema, user_id: int, db: Session = Depends(get_db)) -> ListResponse:
    list_ = delete_list(**list_.dict(), user_id=user_id, db=db)
    if list_ is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Performing an operation on someone else's board",
        )
    else:
        return ListResponse(list_id=list_.id, name=list_.name, board_id=list_.board_id)


def swap_lists_by_ordering_services(list_: Ordering, user_id: int, db: Session = Depends(get_db)) -> str:
    swap_lists_ordering(**list_.dict(), user_id=user_id, db=db)
    return "Ok"
