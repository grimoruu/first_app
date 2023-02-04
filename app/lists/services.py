from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.lists.dao import add_list, delete_list, get_lists, get_lists_ordering, swap_lists_ordering, update_list
from app.lists.schemas import ListResponse, ListSchema
from db.db import get_db


def get_lists_service(board_id: int, user_id: int, db: Session) -> list:
    rows = get_lists(board_id=board_id, user_id=user_id, db=db)
    return [
        ListSchema(
            **_
        )
        for _ in rows
    ]


def create_list_services(name: str, board_id: int, user_id: int, db: Session = Depends(get_db)) -> ListResponse:
    ordering = get_lists_ordering(board_id=board_id, db=db)
    list_ = add_list(name=name, board_id=board_id, ordering=ordering, user_id=user_id, db=db)
    if list_ is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return ListResponse(list_id=list_[0], name=list_[1], board_id=list_[2])


def update_list_services(list_id: int, name: str, board_id: int, user_id: int,
                         db: Session = Depends(get_db)) -> ListResponse:
    list_ = update_list(list_id=list_id, name=name, board_id=board_id, user_id=user_id, db=db)
    if list_ is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return ListResponse(list_id=list_[0], name=list_[1], board_id=list_[2])


def delete_list_services(list_id: int, board_id: int, user_id: int, db: Session = Depends(get_db)) -> ListResponse:
    list_ = delete_list(list_id=list_id, board_id=board_id, user_id=user_id, db=db)
    if list_ is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return ListResponse(list_id=list_[0], name=list_[1], board_id=list_[2])


def swap_lists_by_ordering_services(list_: list, board_id: int, user_id: int, db: Session = Depends(get_db)) -> str:
    swap_lists_ordering(list_=list_, board_id=board_id, user_id=user_id, db=db)
    return "Ok"
