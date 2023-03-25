from decimal import Decimal

from sqlalchemy import desc, exists, func, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from db.models import Board, List


def get_lists(board_id: int, user_id: int) -> Select:
    query = (
        select(List.id, List.name, List.description)
        .join(Board, List.board_id == Board.id)
        .where(List.board_id == board_id, List.is_deleted.is_(False), Board.user_id == user_id)
        .order_by(desc(List.ordering))
    )
    return query


def add_list(name: str, description: str | None, board_id: int, ordering: Decimal, *, db: Session) -> None:
    query = insert(List).values(name=name, description=description, board_id=board_id, ordering=ordering)
    db.execute(query)


def update_list(list_id: int, *, values: dict, db: Session) -> None:
    query = update(List).where(List.id == list_id).values(**values)
    db.execute(query)


def delete_list(list_id: int, *, db: Session) -> None:
    query = update(List).where(List.id == list_id).values(is_deleted=True)
    db.execute(query)


def select_lists_next_ordering(prev_list_ordering: Decimal, board_id: int, *, db: Session) -> Decimal | None:
    query = (
        select(List.ordering)
        .where(List.ordering < prev_list_ordering, List.board_id == board_id)
        .order_by(desc(List.ordering))
        .limit(1)
    )
    return db.execute(query).scalar_one_or_none()


def lists_ordering_update(list_id: int, ordering: Decimal, *, db: Session) -> None:
    query = update(List).where(List.id == list_id).values(ordering=ordering)
    db.execute(query)


def update_board_lists_ordering(board_id: int, *, db: Session) -> None:
    update_subquery = (
        select(List.id, func.row_number().over(order_by=List.ordering).label("row_num"))
        .select_from(List)
        .where(List.board_id == board_id)
        .subquery()
    )
    query = (
        update(List)
        .values(ordering=update_subquery.c.row_num)
        .where(List.board_id == board_id, List.id == update_subquery.c.id)
    )
    db.execute(query)


def get_lists_ordering(board_id: int, *, db: Session) -> Decimal | None:
    query = select(List.ordering).where(List.board_id == board_id).order_by(desc(List.ordering)).limit(1)
    return db.execute(query).scalar_one_or_none()


def check_true_users(list_id: int, board_id: int, user_id: int, *, db: Session) -> bool:
    query = exists(
        select(List.id)
        .join(Board, List.board_id == Board.id)
        .where(Board.id == board_id, Board.user_id == user_id, List.id == list_id)
    ).select()
    return db.execute(query).scalar_one()
