from sqlalchemy import asc, desc, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.models import Board, List


def get_lists_ordering(db: Session) -> int:
    try:
        query = (
            select(List.ordering)
            .order_by(desc(List.ordering))
            .select_from(List)
        )
        return db.execute(query).fetchall()[0][0]
    except IndexError:
        return 0


def add_new_list(user_id: int, board_id: int, name: str, ordering: int, db: Session) -> int | None:
    query_select_user = (
        select(Board.user_id)
        .where(Board.id == board_id)
        .select_from(Board)
    )
    if db.execute(query_select_user).scalar_one() == user_id:
        query = (
            insert(List)
            .values(
                name=name,
                board_id=board_id,
                ordering=ordering + 1
            )
            .returning(List.id)
        )
        return db.execute(query).scalar_one()
    return None


def get_lists(user_id: int, board_id: int, db: Session) -> list[Row]:
    query = (
        select(
            List.id,
            List.name,
            List.board_id,
            List.ordering,
        )
        .join(Board)
        .where(Board.user_id == user_id,
               List.board_id == board_id,
               List.is_deleted == "false")
        .order_by(asc(List.ordering))
        .select_from(List)
    )
    return db.execute(query).fetchall()


def swap_lists_ordering(user_id: int, board_id: int, first_list: int, second_list: int, db: Session) -> str | None:
    query_select_user = (
        select(Board.user_id)
        .where(Board.id == board_id)
        .select_from(Board)
    )
    if db.execute(query_select_user).scalar_one() == user_id:
        query_1 = (
            select(List.ordering)
            .where(List.id == first_list, List.board_id == board_id)
            .select_from(List)
        )
        first_list_ordering = db.execute(query_1).scalar_one()
        query_2 = (
            select(List.ordering)
            .where(List.id == second_list, List.board_id == board_id)
            .select_from(List)
        )
        second_list_ordering = db.execute(query_2).scalar_one()
        query_3 = (
            update(List)
            .where(List.id == second_list, List.board_id == board_id)
            .values(
                ordering=-1
            )
        )
        db.execute(query_3)
        query_4 = (
            update(List)
            .where(List.id == first_list, List.board_id == board_id)
            .values(
                ordering=second_list_ordering
            )
        )
        db.execute(query_4)
        query_5 = (
            update(List)
            .where(List.id == second_list, List.board_id == board_id)
            .values(
                ordering=first_list_ordering
            )
        )
        db.execute(query_5)
        return "lists_swapped"
    return None


def delete_list(user_id: int, board_id: int, list_id: int, db: Session) -> str | None:
    query_select_user = (
        select(Board.user_id)
        .where(Board.id == board_id)
        .select_from(Board)
    )
    if db.execute(query_select_user).scalar_one() == user_id:
        query = (
            update(List)
            .where(List.id == list_id, List.board_id == board_id)
            .values(
                is_deleted=True
            )
            .returning(List.name)
        )
        return db.execute(query).scalar_one()
    else:
        return None


def update_list(user_id: int, board_id: int, list_id: int, name: str, db: Session) -> str | None:
    query_select_user = (
        select(Board.user_id)
        .where(Board.id == board_id)
        .select_from(Board)
    )
    if db.execute(query_select_user).scalar_one() == user_id:
        query = (
            update(List)
            .where(List.board_id == board_id, List.id == list_id)
            .values(
                name=name
            )
            .returning(List.name)
        )
        return db.execute(query).scalar_one()
    else:
        return None
