from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.tasks.dao import check_true_users
from app.users.depends import get_user_by_token
from db.db import get_read_db


def check_users_task_service(
    task_id: int = Path(alias="task_id"),
    list_id: int = Path(alias="list_id"),
    board_id: int = Path(alias="board_id"),
    user_id: int = Depends(get_user_by_token),
    db: Session = Depends(get_read_db),
) -> None:
    if not check_true_users(task_id, list_id, board_id, user_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error in request, please check if the path is correct",
        )
