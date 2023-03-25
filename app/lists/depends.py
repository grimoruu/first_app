from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.lists.dao import check_true_users
from app.users.depends import get_user_by_token
from db.db import get_read_db


def check_users_list_service(
    list_id: int = Path(alias="list_id"),
    board_id: int = Path(alias="board_id"),
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_read_db),
) -> None:
    if not check_true_users(list_id, board_id, user_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error in request, please check if the path is correct",
        )
