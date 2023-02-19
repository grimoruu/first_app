from fastapi import Depends
from sqlalchemy.orm import Session

from app.boards.dao import add_board, delete_board, get_users_board, update_board
from app.boards.schemas import BoardCreateSchema, BoardResponse, BoardSchemaResponse, BoardUpdateSchema
from db.db import get_db


def get_boards_service(user_id: int, db: Session) -> list[BoardSchemaResponse]:
    rows = get_users_board(user_id, db)
    return [BoardSchemaResponse(**row) for row in rows]


def create_board_services(board_: BoardCreateSchema, user_id: int, db: Session) -> BoardResponse:
    board = add_board(**board_.dict(), user_id=user_id, db=db)
    return BoardResponse(board_id=board.id, name=board.name)


def update_board_services(board_id: int, board_: BoardUpdateSchema, user_id: int, db: Session) -> None:
    return update_board(**board_.dict(), board_id=board_id, user_id=user_id, db=db)


def delete_board_services(board_id: int, user_id: int, db: Session = Depends(get_db)) -> None:
    return delete_board(board_id=board_id, user_id=user_id, db=db)
