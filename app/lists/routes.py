from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.boards.depends import check_users_board_service
from app.lists.depends import check_users_list_service
from app.lists.schemas import ListCreateSchema, ListGetDataResponse, ListOrdering, ListUpdateSchema
from app.lists.services import (
    create_list_services,
    delete_list_services,
    get_lists_service,
    lists_ordering_services,
    update_list_services,
)
from app.tasks.routes import router as tasks_router
from app.users.depends import get_user_by_token
from core.pagination.schemas import PaginationParams
from db.db import get_read_db, get_write_db

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=ListGetDataResponse)
def get_lists_api(
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_read_db),
) -> ListGetDataResponse:
    return get_lists_service(board_id, user_id, pagination, db=db)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_list_api(
    board_id: int,
    list_create: ListCreateSchema,
    db: Session = Depends(get_write_db),
    _: None = Depends(check_users_board_service),
) -> None:
    create_list_services(board_id, list_create=list_create, db=db)


@router.patch("/{list_id}", status_code=status.HTTP_200_OK)
def update_list_api(
    list_id: int,
    list_update: ListUpdateSchema,
    db: Session = Depends(get_write_db),
    _: None = Depends(check_users_list_service),
) -> ListUpdateSchema:
    update_list_services(list_id, list_update=list_update.dict(exclude_unset=True), db=db)
    return list_update


@router.delete("/{list_id}", status_code=status.HTTP_200_OK)
def delete_list_api(
    list_id: int,
    db: Session = Depends(get_write_db),
    _: None = Depends(check_users_list_service),
) -> None:
    delete_list_services(list_id, db=db)


@router.post("/{list_id}/ordering", status_code=status.HTTP_200_OK)
def ordering_list_api(
    ordering: ListOrdering,
    list_id: int,
    board_id: int,
    db: Session = Depends(get_write_db),
    _: None = Depends(check_users_list_service),
) -> None:
    lists_ordering_services(ordering.prev_list_ordering, list_id, board_id, db=db)


router.include_router(tasks_router, prefix="/{list_id}/tasks", tags=["task"])
