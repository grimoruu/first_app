from sqlalchemy import desc, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.models import Board, List, Task


def get_task_ordering(list_id: int, board_id: int, db: Session) -> int:
    try:
        query = (
            select(Task.ordering)
            .join(List)
            .where(Task.list_id == list_id, List.board_id == board_id)
            .order_by(desc(Task.ordering))
        )
        return db.execute(query).fetchall()[0][0] + 1
    except IndexError:
        return 1


def check_true_users(list_id: int, board_id: int, user_id: int, db: Session) -> bool:
    query_select_user = select(Board.user_id).join(List).where(Board.id == board_id, List.id == list_id)
    if db.execute(query_select_user).scalar_one() == user_id:
        return True
    else:
        return False


def get_tasks(list_id: int, board_id: int, user_id: int, db: Session) -> list[Row]:
    query = (
        select(
            Task.id,
            Task.name,
            Task.description,
            Task.list_id,
            Task.ordering,
        )
        .join(List, Task.list_id == List.id)
        .join(Board, List.board_id == Board.id)
        .where(
            List.id == list_id,
            Board.id == board_id,
            Board.user_id == user_id,
            Task.is_deleted.is_(False),
        )
        .order_by(Task.ordering)
    )
    return db.execute(query).fetchall()


def add_task(
    name: str,
    description: str,
    list_id: int,
    ordering: int,
    board_id: int,
    user_id: int,
    db: Session,
) -> Row | None:
    if check_true_users(list_id=list_id, board_id=board_id, user_id=user_id, db=db):
        query = (
            insert(Task)
            .values(name=name, description=description, list_id=list_id, ordering=ordering)
            .returning(Task.id, Task.name, Task.description, Task.list_id)
        )
        return db.execute(query).fetchone()
    else:
        return None


def update_task(
    task_id: int,
    name: str,
    description: str,
    list_id: int,
    board_id: int,
    user_id: int,
    db: Session,
) -> Row | None:
    if check_true_users(list_id=list_id, board_id=board_id, user_id=user_id, db=db):
        query = (
            update(Task)
            .where(Task.id == task_id)
            .values(name=name, description=description)
            .returning(Task.id, Task.name, Task.description, Task.list_id)
        )
        return db.execute(query).fetchone()
    else:
        return None


def delete_task(task_id: int, list_id: int, board_id: int, user_id: int, db: Session) -> Row | None:
    if check_true_users(list_id=list_id, board_id=board_id, user_id=user_id, db=db):
        query = (
            update(Task)
            .where(Task.id == task_id)
            .values(is_deleted=True)
            .returning(Task.id, Task.name, Task.description, Task.list_id)
        )
        return db.execute(query).fetchone()
    else:
        return None
