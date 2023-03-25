from decimal import Decimal

from sqlalchemy import desc, exists, func, insert, select, true, update
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import Select
from sqlalchemy.sql.functions import count

from db.models import Board, List, Task


def get_tasks(list_id: list, board_id: int, user_id: int, limit: int, offset: int) -> Select:
    t_outer = aliased(Task)
    t_inner = aliased(Task)
    subquery = (
        select(t_inner.id, func.count().over().label("total"))
        .join(List, t_inner.list_id == List.id)
        .join(Board, List.board_id == Board.id)
        .where(
            t_inner.list_id == t_outer.list_id,
            Board.user_id == user_id,
            Board.id == board_id,
            t_inner.is_deleted.is_(False),
        )
        .order_by(desc(List.ordering), (desc(t_inner.ordering)))
        .limit(limit)
        .offset(offset)
        .subquery()
        .lateral()
    )
    query = (
        select(t_outer.name, t_outer.description, t_outer.list_id, subquery.c.total)
        .select_from(t_outer)
        .join(List, t_outer.list_id == List.id)
        .outerjoin(subquery, true())
        .where(t_outer.list_id.in_(list_id), t_outer.id == subquery.c.id)
        .order_by(desc(List.ordering), (desc(t_outer.ordering)))
    )
    return query


def count_of_list_tasks(list_id: list, board_id: int, user_id: int, *, db: Session) -> int:
    query = (
        select(count(Task.id))
        .join(List)
        .join(Board, List.board_id == Board.id)
        .where(
            Task.is_deleted.is_(False),
            Task.list_id.in_(list_id),
            Board.id == board_id,
            Board.user_id == user_id,
        )
    )
    return db.execute(query).scalar_one()


def add_task(name: str, description: str | None, list_id: int, ordering: Decimal, *, db: Session) -> None:
    query = insert(Task).values(name=name, description=description, list_id=list_id, ordering=ordering)
    db.execute(query)


def update_task(task_id: int, *, values: dict, db: Session) -> None:
    query = update(Task).where(Task.id == task_id).values(**values)
    db.execute(query)


def delete_task(task_id: int, *, db: Session) -> None:
    query = update(Task).where(Task.id == task_id).values(is_deleted=True)
    db.execute(query)


def select_tasks_next_ordering(prev_task_ordering: Decimal, new_list_id: int, *, db: Session) -> Decimal | None:
    query = (
        select(Task.ordering)
        .where(Task.ordering < prev_task_ordering, Task.list_id == new_list_id)
        .order_by(desc(Task.ordering))
        .limit(1)
    )
    return db.execute(query).scalar_one_or_none()


def tasks_ordering_update(task_id: int, ordering: Decimal, new_list_id: int, *, db: Session) -> None:
    query = update(Task).where(Task.id == task_id).values(list_id=new_list_id, ordering=ordering)
    db.execute(query)


def update_all_task_ordering(list_id: int, *, db: Session) -> None:
    subquery = (
        select(Task.id, func.row_number().over(order_by=Task.ordering).label("row_num"))
        .select_from(Task)
        .where(Task.list_id == list_id)
        .subquery()
    )
    query = update(Task).values(ordering=subquery.c.row_num).where(Task.list_id == list_id, Task.id == subquery.c.id)
    db.execute(query)


def get_task_ordering(list_id: int, *, db: Session) -> Decimal | None:
    query = (
        select(Task.ordering)
        .join(List, Task.list_id == List.id)
        .where(Task.list_id == list_id)
        .order_by(desc(Task.ordering))
        .limit(1)
    )
    return db.execute(query).scalar_one_or_none()


def check_true_users(task_id: int, list_id: int, board_id: int, user_id: int, *, db: Session) -> bool:
    query = exists(
        select(Task.id)
        .join(List, Task.list_id == List.id)
        .join(Board, List.board_id == Board.id)
        .where(Task.id == task_id, List.id == list_id, Board.id == board_id, Board.user_id == user_id)
    ).select()
    return db.execute(query).scalar_one()
