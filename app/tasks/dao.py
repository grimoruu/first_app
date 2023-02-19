from sqlalchemy import desc, func, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session, aliased

from db.models import Board, List, Task


def get_task_ordering(list_id: int, db: Session) -> float | None:
    query = select(Task.ordering).join(List).where(Task.list_id == list_id).order_by(desc(Task.ordering)).limit(1)
    return db.execute(query).scalar_one_or_none()


def check_true_users(list_id: int, board_id: int, db: Session) -> int | None:
    return db.execute(
        select(Board.user_id).join(List).where(Board.id == board_id, List.id == list_id)
    ).scalar_one_or_none()


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


def add_task(name: str, description: str, list_id: int, ordering: float, db: Session) -> None:
    query = insert(Task).values(name=name, description=description, list_id=list_id, ordering=ordering)
    db.execute(query)


def update_task(name: str, description: str, task_id: int, db: Session) -> None:
    query = update(Task).where(Task.id == task_id).values(name=name, description=description)
    db.execute(query)


def delete_task(task_id: int, db: Session) -> None:
    query = update(Task).where(Task.id == task_id).values(is_deleted=True)
    db.execute(query)


def select_tasks_next_ordering(prev_task_ordering: float, new_list_id: int, db: Session) -> float | None:
    query = (
        select(Task.ordering)
        .where(Task.ordering < prev_task_ordering, Task.list_id == new_list_id)
        .order_by(desc(Task.ordering))
        .limit(1)
    )
    return db.execute(query).scalar_one_or_none()


def tasks_ordering_change(task_id: int, ordering: float, new_list_id: int, db: Session) -> float:
    query = (
        update(Task).where(Task.id == task_id).values(list_id=new_list_id, ordering=ordering).returning(Task.ordering)
    )
    return db.execute(query).scalar_one()


def update_all_task_ordering(list_id: int, db: Session) -> None:
    subq = select(Task.id, func.row_number().over(order_by=Task.ordering).label("row_num")).select_from(Task)\
        .where(Task.list_id == list_id).subquery()
    query = update(Task).values(ordering=subq.c.row_num).where(Task.list_id == list_id, Task.id == subq.c.id)
    db.execute(query)

