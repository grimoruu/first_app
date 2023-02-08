from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.lists.schemas import (
    ListCreateSchema,
    ListDeleteSchema,
    ListResponse,
    ListSchema,
    ListsGetSchema,
    ListUpdateSchema,
    Ordering,
)
from app.lists.services import (
    create_list_services,
    delete_list_services,
    get_lists_service,
    swap_lists_by_ordering_services,
    update_list_services,
)
from core.auth_utils.auth import get_user_by_token
from db.db import get_db

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=list[ListSchema])
def get_boards_all_lists_api(
    list_: ListsGetSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> list[ListSchema]:
    return get_lists_service(list_=list_, user_id=user_id, db=db)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ListResponse)
def create_list_api(
    list_: ListCreateSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> ListResponse:
    return create_list_services(list_=list_, user_id=user_id, db=db)


@router.patch("", status_code=status.HTTP_200_OK, response_model=ListResponse)
def update_list_api(
    list_: ListUpdateSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> ListResponse:
    return update_list_services(list_=list_, user_id=user_id, db=db)


@router.delete("", status_code=status.HTTP_200_OK, response_model=ListResponse)
def delete_list_api(
    list_: ListDeleteSchema,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> ListResponse:
    return delete_list_services(list_=list_, user_id=user_id, db=db)


@router.put("/order", status_code=status.HTTP_200_OK)
def swap_list_api(
    list_: Ordering,
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_db),
) -> str:
    return swap_lists_by_ordering_services(list_=list_, user_id=user_id, db=db)
