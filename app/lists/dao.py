from decimal import Decimal
from typing import Literal

from sqlalchemy import desc, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from app.boards.dao import fetch_one_
from db.models import Board, List


def get_lists(board_id: int, user_id: int, db: Session) -> list[Row]:
    query = (
        select(
            List.id,
            List.name,
            List.board_id,
            List.ordering,
        )
        .join(Board)
        .where(
            Board.user_id == user_id,
            List.board_id == board_id,
            List.is_deleted.is_(False),
        )
        .order_by(List.ordering)
        .limit(2)
    )
    return db.execute(query).fetchall()


def add_list(name: str, board_id: int, ordering: int, user_id: int, db: Session) -> Row | Literal[False]:
    if check_true_users(board_id=board_id, user_id=user_id, db=db):
        query = (
            insert(List)
            .values(name=name, board_id=board_id, ordering=ordering)
            .returning(List.id, List.name, List.board_id)
        )
        return fetch_one_(query, db)
    else:
        return False


def update_list(list_id: int, name: str, board_id: int, user_id: int, db: Session) -> None | Literal[False]:
    if check_true_users(board_id=board_id, user_id=user_id, db=db):
        query = (
            update(List)
            .where(
                List.id == list_id,
                List.board_id == board_id,
            )
            .values(name=name)
        )
        db.execute(query)
        return None
    else:
        return False


def delete_list(list_id: int, board_id: int, user_id: int, db: Session) -> None | Literal[False]:
    if check_true_users(board_id=board_id, user_id=user_id, db=db):
        query = (
            update(List)
            .where(List.id == list_id, List.board_id == board_id)
            .values(is_deleted=True)
            .returning(List.id, List.name, List.board_id)
        )
        db.execute(query)
        return None
    else:
        return False


def get_lists_ordering(board_id: int, db: Session) -> int:
    query = select(List.ordering).where(List.board_id == board_id).order_by(desc(List.ordering)).limit(1)
    last_ordering = db.execute(query).scalar_one_or_none()
    return last_ordering + 1 if last_ordering else 1


def check_true_users(board_id: int, user_id: int, db: Session) -> bool:
    query_select_user = select(Board.user_id).where(Board.id == board_id)
    return True if db.execute(query_select_user).scalar_one() == user_id else False


def lists_ordering_change(
    prev_list_ordering: float, list_id: int, board_id: int, user_id: int, db: Session
) -> None | Literal[False]:
    if check_true_users(board_id=board_id, user_id=user_id, db=db):
        try:
            select_next_ord = (
                select(List.ordering).where(List.ordering > prev_list_ordering).order_by(List.ordering).limit(1)
            )
            next_list_ordering = db.execute(select_next_ord).scalar_one()
        except NoResultFound:
            next_list_ordering = prev_list_ordering + 1
        ordering_ = (next_list_ordering + prev_list_ordering) / 2
        query = update(List).where(List.id == list_id).values(ordering=ordering_).returning(List.ordering)
        res = db.execute(query).scalar_one()
        if Decimal(str(res)).as_tuple().exponent * (-1) > 15:
            count_of_lists = select(func.count(List.ordering)).select_from(List).where(List.board_id == board_id)
            count_lists = db.execute(count_of_lists).scalar_one()
            ordering = select(List.id).order_by(List.ordering).where(List.board_id == board_id)
            old_ordering = db.execute(ordering).fetchall()
            for i in range(0, count_lists):
                update_query = update(List).where(List.id == old_ordering[i][0]).values(ordering=(i + 1))
                db.execute(update_query)
        return None
    else:
        return False
