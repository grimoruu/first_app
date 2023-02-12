from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.boards.schemas import BoardCreateSchema, BoardResponse, BoardSchemaResponse, BoardUpdateSchema
from app.boards.services import create_board_services, delete_board_services, get_boards_service, update_board_services
from app.lists.routes import router as lists_router
from core.auth_utils.auth import get_user_by_token
from db.db import get_db


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=list[BoardSchemaResponse])
def get_users_all_boards_api(
    user_id: int = Depends(get_user_by_token), db: Session = Depends(get_db)
) -> list[BoardSchemaResponse]:
    return get_boards_service(user_id=user_id, db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BoardResponse)
def create_board_api(
    board: BoardCreateSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> BoardResponse:
    return create_board_services(board_=board, user_id=user_id, db=db)


@router.patch("/{board_id}", status_code=status.HTTP_200_OK)
def update_board_api(
    board_id: int,
    board: BoardUpdateSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> None:
    return update_board_services(board_id=board_id, board_=board, user_id=user_id, db=db)


@router.delete("/{board_id}", status_code=status.HTTP_200_OK)
def delete_board_api(
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> None:
    return delete_board_services(board_id=board_id, user_id=user_id, db=db)


router.include_router(lists_router, prefix="/{board_id}/lists", tags=["list"])
