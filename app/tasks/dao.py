from sqlalchemy import desc, insert, select, update, asc
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.models import List, Task, Board


def get_task_ordering(db: Session) -> int:
    try:
        query = (
            select(Task.ordering)
            .order_by(desc(Task.ordering))
            .select_from(Task)
        )
        return db.execute(query).fetchall()[0][0]
    except IndexError:
        return 0


def check_true_users(user_id: int, board_id: int, list_id: int, db: Session) -> bool:
    query_select_user = (
        select(Board.user_id)
        .join(List)
        .where(Board.id == board_id, List.id == list_id)
        .select_from(Board)
    )
    result = db.execute(query_select_user).scalar_one()
    if result == user_id:
        return True
    else:
        return False


def get_tasks(user_id: int, board_id: int, list_id: int, db: Session) -> list[Row]:
    query = (
        select(
            Task.id,
            Task.name,
            Task.description,
            Task.list_id,
            Task.ordering,
        )
        .select_from(Task)
        .join(List, Task.list_id == List.id)
        .join(Board, List.board_id == Board.id)
        .where(List.id == list_id,
               Board.id == board_id,
               Board.user_id == user_id,
               Task.is_deleted.is_(False))
        .order_by(Task.ordering)
    )
    return db.execute(query).fetchall()


def add_new_task(user_id: int, board_id: int, list_id: int,
                 name: str, description: str, ordering: int, db: Session) -> int | None:

    if check_true_users(user_id, board_id, list_id, db):
        query = (
            insert(Task)
            .values(
                name=name,
                description=description,
                list_id=list_id,
                ordering=ordering + 1
            )
            .returning(Task.id)
        )
        return db.execute(query).scalar_one()
    else:
        return None


def update_task(user_id: int, board_id: int, list_id: int,
                task_id: int, task_name: str, task_description: str, db: Session) -> int | None:

    if check_true_users(user_id, board_id, list_id, db):
        query = (
            update(Task)
            .where(Task.id == task_id)
            .values(
                name=task_name,
                description=task_description
            )
            .returning(Task.id)
        )
        return db.execute(query).scalar_one()
    else:
        return None


def delete_task(user_id: int, board_id: int, list_id: int, task_id: int, db: Session) -> Row | None:
    if check_true_users(user_id, board_id, list_id, db):
        query = (
            update(Task)
            .where(Task.id == task_id)
            .values(
                is_deleted=True
            )
            .returning(Task.name, Task.description)
        )
        return db.execute(query).fetchall()[0]
    else:
        return None
