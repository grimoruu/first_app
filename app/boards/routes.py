from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.boards.depends import check_users_board_service
from app.boards.schemas import (
    BoardCreateSchema,
    BoardGetDataResponse,
    BoardsSchemaResponse,
    BoardUpdateSchema,
)
from app.boards.services import (
    create_board_services,
    delete_board_services,
    get_boards_data_service,
    get_boards_service,
    update_board_services,
)
from app.lists.routes import router as lists_router
from app.users.depends import get_user_by_token
from core.pagination.schemas import PaginationParams
from db.db import get_read_db, get_write_db

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=BoardsSchemaResponse)
def get_boards_api(
    user_id: int = Depends(get_user_by_token),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_read_db),
) -> BoardsSchemaResponse:
    return get_boards_service(user_id, pagination, db=db)


@router.get("/{board_id}", status_code=status.HTTP_200_OK, response_model=BoardGetDataResponse)
def get_boards_data_api(
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_read_db),
) -> BoardGetDataResponse:
    return get_boards_data_service(board_id, user_id, pagination, db=db)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_board_api(
    board_create: BoardCreateSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_write_db),
) -> None:
    create_board_services(board_create, user_id, db=db)


@router.patch("/{board_id}", status_code=status.HTTP_200_OK)
def update_board_api(
    board_id: int,
    board_update: BoardUpdateSchema,
    user_id: int = Depends(get_user_by_token),
    _: None = Depends(check_users_board_service),
    db: Session = Depends(get_write_db),
) -> BoardUpdateSchema:
    update_board_services(board_id, board_update.dict(exclude_unset=True), user_id, db=db)
    return board_update


@router.delete("/{board_id}", status_code=status.HTTP_200_OK)
def delete_board_api(
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    _: None = Depends(check_users_board_service),
    db: Session = Depends(get_write_db),
) -> None:
    delete_board_services(board_id, user_id, db=db)


router.include_router(lists_router, prefix="/{board_id}/lists", tags=["list"])
