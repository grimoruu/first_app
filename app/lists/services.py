from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.lists.dao import add_list, delete_list, get_lists, get_lists_ordering, lists_ordering_change, update_list
from app.lists.schemas import ListCreateSchema, ListResponse, ListSchemaResponse, ListUpdateSchema
from db.db import get_db


def get_lists_service(board_id: int, user_id: int, db: Session = Depends(get_db)) -> list[ListSchemaResponse]:
    rows = get_lists(board_id, user_id, db)
    return [ListSchemaResponse(**_) for _ in rows]


def create_list_services(
    board_id: int, list_: ListCreateSchema, user_id: int, db: Session = Depends(get_db)
) -> ListResponse:
    ordering = get_lists_ordering(board_id=board_id, db=db)
    lists = add_list(**list_.dict(), board_id=board_id, ordering=ordering, user_id=user_id, db=db)
    if lists is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Performing an operation on someone else's board",
        )
    else:
        return ListResponse(list_id=lists.id, name=lists.name, board_id=lists.board_id)


def update_list_services(
    list_id: int, list_: ListUpdateSchema, board_id: int, user_id: int, db: Session = Depends(get_db)
) -> None:
    lists = update_list(list_id=list_id, **list_.dict(), board_id=board_id, user_id=user_id, db=db)
    if lists is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Performing an operation on someone else's board",
        )
    else:
        return lists


def delete_list_services(list_id: int, board_id: int, user_id: int, db: Session = Depends(get_db)) -> None:
    lists = delete_list(list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    if lists is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Performing an operation on someone else's board",
        )
    else:
        return lists


def lists_ordering_services(
    prev_list_ordering: float, list_id: int, board_id: int, user_id: int, db: Session = Depends(get_db)
) -> None:
    orderings = lists_ordering_change(
        prev_list_ordering=prev_list_ordering, list_id=list_id, board_id=board_id, user_id=user_id, db=db
    )
    if orderings is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Performing an operation on someone else's board",
        )
    else:
        return orderings
