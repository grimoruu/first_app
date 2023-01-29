from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.lists.schemas import ListNameSchema, ListResponse, ListSchema
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


@router.get("/{board_id}/lists", status_code=status.HTTP_200_OK, response_model=list[ListSchema])
def get_boards_all_lists_api(board_id: int,
                             user_id: int = Depends(get_user_by_token),
                             db: Session = Depends(get_db)) -> list[ListSchema]:
    return get_lists_service(user_id=user_id, board_id=board_id, db=db)


@router.post("/{board_id}/lists/create", status_code=status.HTTP_201_CREATED, response_model=ListResponse)
def create_list_api(board_id: int,
                    name: ListNameSchema,
                    db: Session = Depends(get_db),
                    user_id: int = Depends(get_user_by_token)) -> ListResponse:
    return create_list_services(user_id=user_id, board_id=board_id, name=name, db=db)


@router.put("/{board_id}/lists/swap-{first_list}-to-{second_list}", status_code=status.HTTP_200_OK)
def swap_list_api(board_id: int,
                  first_list: int,
                  second_list: int,
                  db: Session = Depends(get_db),
                  user_id: int = Depends(get_user_by_token)) -> str:
    return swap_lists_by_ordering_services(user_id=user_id,
                                           board_id=board_id,
                                           first_list=first_list,
                                           second_list=second_list,
                                           db=db)


@router.delete("/{board_id}/lists/delete/{list_id}",
               status_code=status.HTTP_200_OK, response_model=ListResponse)
def delete_list_api(board_id: int,
                    list_id: int,
                    db: Session = Depends(get_db),
                    user_id: int = Depends(get_user_by_token)) -> ListResponse:
    return delete_list_services(user_id=user_id,
                                board_id=board_id,
                                list_id=list_id,
                                db=db)


@router.put("/{board_id}/lists/update/{list_id}",
            status_code=status.HTTP_200_OK, response_model=ListResponse)
def update_list_api(board_id: int,
                    list_id: int,
                    name: ListNameSchema,
                    db: Session = Depends(get_db),
                    user_id: int = Depends(get_user_by_token)) -> ListResponse:
    return update_list_services(user_id=user_id,
                                board_id=board_id,
                                list_id=list_id,
                                name=name,
                                db=db)
