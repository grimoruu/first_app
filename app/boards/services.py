from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.boards.dao import add_new_board, check_board_exist, delete_board, get_users_board, update_boards_name
from app.boards.schemas import BoardNameResponse, BoardNameSchema, BoardResponse, BoardSchema
from db.db import get_db


def get_boards_service(user_id: int,
                       db: Session = Depends(get_db)) -> list[BoardSchema]:
    rows = get_users_board(user_id, db)
    return [
        BoardSchema(
            **_
        )
        for _ in rows
    ]


def create_board_services(name: BoardNameSchema,
                          user_id: int,
                          db: Session = Depends(get_db)) -> BoardResponse:
    board_id = add_new_board(name.name, user_id, db)
    return BoardResponse(board_id=board_id, name=name.name)


def update_board_services(board_id: int,
                          name: BoardNameSchema,
                          user_id: int,
                          db: Session = Depends(get_db)) -> BoardNameResponse:
    board_name = update_boards_name(board_id=board_id, name=name.name, user_id=user_id, db=db)
    return BoardNameResponse(name=board_name)


def delete_board_services(board_id: int,
                          user_id: int,
                          db: Session = Depends(get_db)) -> BoardNameResponse:
    try:
        if check_board_exist(board_id=board_id, user_id=user_id, db=db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Board already deleted')
        else:
            board_name = delete_board(user_id=user_id, board_id=board_id, db=db)
            return BoardNameResponse(name=board_name)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Board dont exist')
