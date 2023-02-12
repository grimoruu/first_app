from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.lists.schemas import ListCreateSchema, ListOrdering, ListResponse, ListSchemaResponse, ListUpdateSchema
from app.lists.services import (
    create_list_services,
    delete_list_services,
    get_lists_service,
    lists_ordering_services,
    update_list_services,
)
from app.tasks.routes import router as tasks_router
from core.auth_utils.auth import get_user_by_token
from db.db import get_db

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=list[ListSchemaResponse])
def get_boards_all_lists_api(
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> list[ListSchemaResponse]:
    return get_lists_service(board_id=board_id, user_id=user_id, db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ListResponse)
def create_list_api(
    board_id: int,
    list_: ListCreateSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> ListResponse:
    return create_list_services(board_id=board_id, list_=list_, user_id=user_id, db=db)


@router.patch("/{list_id}", status_code=status.HTTP_200_OK)
def update_list_api(
    list_id: int,
    board_id: int,
    list_: ListUpdateSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> None:
    return update_list_services(list_id=list_id, list_=list_, board_id=board_id, user_id=user_id, db=db)


@router.delete("/{list_id}", status_code=status.HTTP_200_OK)
def delete_list_api(
    list_id: int,
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> None:
    return delete_list_services(list_id=list_id, board_id=board_id, user_id=user_id, db=db)


@router.patch("/{list_id}/ordering", status_code=status.HTTP_200_OK)
def ordering_list_api(
    ordering: ListOrdering,
    list_id: int,
    board_id: int,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> None:
    return lists_ordering_services(
        prev_list_ordering=ordering.prev_list_ordering, list_id=list_id, board_id=board_id, user_id=user_id, db=db
    )


router.include_router(tasks_router, prefix="/{list_id}/tasks", tags=["task"])
