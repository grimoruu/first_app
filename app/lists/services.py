from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.lists.dao import add_new_list, delete_list, get_lists, get_lists_ordering, swap_lists_ordering, update_list
from app.lists.schemas import ListNameSchema, ListResponse, ListSchema
from db.db import get_db


def get_lists_service(user_id: int, board_id: int, db: Session) -> list:
    rows = get_lists(user_id, board_id, db)
    return [
        ListSchema(
            **_
        )
        for _ in rows
    ]


def create_list_services(user_id: int,
                         board_id: int,
                         name: ListNameSchema,
                         db: Session = Depends(get_db)) -> ListResponse:
    ordering = get_lists_ordering(db=db)
    list_id = add_new_list(user_id, board_id, name.name, ordering, db)
    if list_id is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return ListResponse(list_id=list_id, board_id=board_id, name=name.name)


def swap_lists_by_ordering_services(user_id: int,
                                    board_id: int,
                                    first_list: int,
                                    second_list: int,
                                    db: Session = Depends(get_db)) -> str:
    swap_status = swap_lists_ordering(user_id=user_id,
                                      board_id=board_id,
                                      first_list=first_list,
                                      second_list=second_list,
                                      db=db)

    if swap_status is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return swap_status


def delete_list_services(user_id: int,
                         board_id: int,
                         list_id: int,
                         db: Session = Depends(get_db)) -> ListResponse:
    list_name = delete_list(user_id=user_id, board_id=board_id, list_id=list_id, db=db)
    if list_name is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return ListResponse(list_id=list_id, board_id=board_id, name=list_name)


def update_list_services(user_id: int,
                         board_id: int,
                         list_id: int,
                         name: ListNameSchema,
                         db: Session = Depends(get_db)) -> ListResponse:
    list_name = update_list(user_id=user_id, board_id=board_id, list_id=list_id, name=name.name, db=db)
    if list_name is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return ListResponse(list_id=list_id, board_id=board_id, name=list_name)
