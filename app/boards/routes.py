from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.boards.schemas import BoardCreateSchema, BoardDeleteSchema, BoardResponse, BoardSchema, BoardUpdateSchema
from app.boards.services import create_board_services, delete_board_services, get_boards_service, update_board_services
from core.auth_utils.auth import get_user_by_token
from db.db import get_db

router = APIRouter()


@router.get("", response_model=list[BoardSchema])
def get_users_all_boards_api(user_id: int = Depends(get_user_by_token),
                             db: Session = Depends(get_db)) -> list[BoardSchema]:
    return get_boards_service(user_id=user_id, db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BoardResponse)
def create_board_api(board: BoardCreateSchema,
                     user_id: int = Depends(get_user_by_token),
                     db: Session = Depends(get_db)) -> BoardResponse:
    return create_board_services(name=board.name, user_id=user_id, db=db)


@router.patch("", status_code=status.HTTP_200_OK, response_model=BoardResponse)
def update_board_api(board: BoardUpdateSchema,
                     user_id: int = Depends(get_user_by_token),
                     db: Session = Depends(get_db)) -> BoardResponse:
    return update_board_services(board_id=board.board_id, name=board.name, user_id=user_id, db=db)


@router.delete("", status_code=status.HTTP_200_OK, response_model=BoardResponse)
def delete_board_api(board: BoardDeleteSchema,
                     user_id: int = Depends(get_user_by_token),
                     db: Session = Depends(get_db)) -> BoardResponse:
    return delete_board_services(board_id=board.board_id, user_id=user_id, db=db)
