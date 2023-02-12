from decimal import Decimal
from typing import Literal

from sqlalchemy import desc, func, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.boards.dao import fetch_one_
from db.models import Board, List, Task


def get_task_ordering(list_id: int, board_id: int, db: Session) -> int:
    try:
        query = (
            select(Task.ordering)
            .join(List)
            .where(Task.list_id == list_id, List.board_id == board_id)
            .order_by(desc(Task.ordering))
            .limit(1)
        )
        return db.execute(query).scalar_one() + 1
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
) -> Row | Literal[False]:
    if check_true_users(list_id=list_id, board_id=board_id, user_id=user_id, db=db):
        query = (
            insert(Task)
            .values(name=name, description=description, list_id=list_id, ordering=ordering)
            .returning(Task.id, Task.name, Task.description, Task.list_id)
        )
        return fetch_one_(query, db)
    else:
        return False


def update_task(
    name: str,
    description: str,
    task_id: int,
    list_id: int,
    board_id: int,
    user_id: int,
    db: Session,
) -> None | Literal[False]:
    if check_true_users(list_id=list_id, board_id=board_id, user_id=user_id, db=db):
        query = update(Task).where(Task.id == task_id).values(name=name, description=description)
        db.execute(query)
        return None
    else:
        return False


def delete_task(task_id: int, list_id: int, board_id: int, user_id: int, db: Session) -> None | Literal[False]:
    if check_true_users(list_id=list_id, board_id=board_id, user_id=user_id, db=db):
        query = update(Task).where(Task.id == task_id).values(is_deleted=True)
        db.execute(query)
        return None
    else:
        return False


def tasks_ordering_change(
    prev_task_ordering: float, new_list_id: int, task_id: int, list_id: int, board_id: int, user_id: int, db: Session
) -> None | Literal[False]:
    if check_true_users(list_id=list_id, board_id=board_id, user_id=user_id, db=db):
        try:
            select_next_ord = (
                select(Task.ordering)
                .where(Task.ordering > prev_task_ordering, Task.list_id == new_list_id)
                .order_by(Task.ordering)
                .limit(1)
            )
            next_task_ordering = db.execute(select_next_ord).scalar_one()
        except NoResultFound:
            try:
                select_next_ord = (
                    select(Task.ordering)
                    .where(Task.ordering == prev_task_ordering, Task.list_id == new_list_id)
                    .order_by(Task.ordering)
                    .limit(1)
                )
                next_task_ordering = db.execute(select_next_ord).scalar_one() + 1
            except NoResultFound:
                next_task_ordering = 2
        ordering_ = (next_task_ordering + prev_task_ordering) / 2
        query = (
            update(Task)
            .where(Task.id == task_id)
            .values(list_id=new_list_id, ordering=ordering_)
            .returning(Task.ordering)
        )
        res = db.execute(query).scalar_one()
        if Decimal(str(res)).as_tuple().exponent * (-1) > 8:
            count_of_tasks = select(func.count(Task.ordering)).select_from(Task).where(Task.list_id == new_list_id)
            count_tasks = db.execute(count_of_tasks).scalar_one()
            ordering = select(Task.id).order_by(Task.ordering).where(Task.list_id == new_list_id)
            old_ordering = db.execute(ordering).fetchall()
            for i in range(0, count_tasks):
                update_query = update(Task).where(Task.id == old_ordering[i][0]).values(ordering=(i + 1))
                db.execute(update_query)
        return None
    else:
        return False
