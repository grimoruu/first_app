from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.boards.schemas import BoardNameResponse, BoardNameSchema, BoardResponse, BoardSchema
from app.boards.services import create_board_services, delete_board_services, get_boards_service, update_board_services
from core.auth_utils.auth import get_user_by_token
from db.db import get_db

router = APIRouter()


@router.get("", response_model=list[BoardSchema])
def get_users_all_boards_api(user_id: int = Depends(get_user_by_token),
                             db: Session = Depends(get_db)) -> list[BoardSchema]:
    return get_boards_service(user_id=user_id, db=db)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=BoardResponse)
def create_board_api(name: BoardNameSchema,
                     user_id: int = Depends(get_user_by_token),
                     db: Session = Depends(get_db)) -> BoardResponse:
    return create_board_services(name=name, user_id=user_id, db=db)


@router.put("/update/{board_id}", status_code=status.HTTP_200_OK, response_model=BoardNameResponse)
def update_board_api(board_id: int,
                     name: BoardNameSchema,
                     user_id: int = Depends(get_user_by_token),
                     db: Session = Depends(get_db)) -> BoardNameResponse:
    return update_board_services(board_id=board_id, name=name, user_id=user_id, db=db)


@router.delete("/delete/{board_id}", status_code=status.HTTP_200_OK, response_model=BoardNameResponse)
def delete_board_api(board_id: int,
                     user_id: int = Depends(get_user_by_token),
                     db: Session = Depends(get_db)) -> BoardNameResponse:
    return delete_board_services(board_id=board_id, user_id=user_id, db=db)
