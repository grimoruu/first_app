from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.boards.dao import add_board, check_board_exist, delete_board, get_users_board, update_board
from app.boards.schemas import BoardResponse, BoardSchema
from db.db import get_db


def get_boards_service(user_id: int, db: Session = Depends(get_db)) -> list[BoardSchema]:
    rows = get_users_board(user_id, db)
    return [
        BoardSchema(
            **_
        )
        for _ in rows
    ]


def create_board_services(name: str, user_id: int, db: Session = Depends(get_db)) -> BoardResponse:
    board = add_board(name=name, user_id=user_id, db=db)
    if board is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return BoardResponse(board_id=board[0], name=board[1])


def update_board_services(board_id: int, name: str, user_id: int, db: Session = Depends(get_db)) -> BoardResponse:
    board = update_board(board_id=board_id, name=name, user_id=user_id, db=db)
    if board is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Performing an operation on someone else's board")
    else:
        return BoardResponse(board_id=board[0], name=board[1])


def delete_board_services(board_id: int, user_id: int, db: Session = Depends(get_db)) -> BoardResponse:
    if check_board_exist(board_id=board_id, user_id=user_id, db=db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Board already deleted')
    else:
        board = delete_board(board_id=board_id, user_id=user_id, db=db)
        if board is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Board dont exist")
        else:
            return BoardResponse(board_id=board[0], name=board[1])
