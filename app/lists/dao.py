from sqlalchemy import desc, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.models import Board, List


def check_true_users(board_id: int, db: Session) -> int | None:
    return db.execute(select(Board.user_id).where(Board.id == board_id)).scalar_one_or_none()


def get_lists_ordering(board_id: int, db: Session) -> int | None:
    query = select(List.ordering).where(List.board_id == board_id).order_by(desc(List.ordering)).limit(1)
    return db.execute(query).scalar_one_or_none()


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
    )
    return db.execute(query).fetchall()


def add_list(name: str, board_id: int, ordering: int, db: Session) -> None:
    query = insert(List).values(name=name, board_id=board_id, ordering=ordering)
    db.execute(query)


def update_list(list_id: int, name: str, db: Session) -> None:
    query = update(List).where(List.id == list_id).values(name=name)
    db.execute(query)


def delete_list(list_id: int, db: Session) -> None:
    query = update(List).where(List.id == list_id).values(is_deleted=True)
    db.execute(query)


def select_lists_next_ordering(prev_list_ordering: float, board_id: int, db: Session) -> float | None:
    query = (
        select(List.ordering)
        .where(List.ordering < prev_list_ordering, List.board_id == board_id)
        .order_by(desc(List.ordering))
        .limit(1)
    )
    return db.execute(query).scalar_one_or_none()


def lists_ordering_change(list_id: int, ordering: float, db: Session) -> float:
    query = update(List).where(List.id == list_id).values(ordering=ordering).returning(List.ordering)
    return db.execute(query).scalar_one()


def update_all_lists_ordering(board_id: int, db: Session) -> None:
    pass
