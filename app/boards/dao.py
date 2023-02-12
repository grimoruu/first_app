from typing import Any

from sqlalchemy import exists, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from core.db_utils import to_nested_list
from db.models import Board, User


def get_users_board(user_id: int, db: Session) -> list[dict]:
    query = (
        select(
            Board.id,
            Board.name,
            User.id.label("user__id"),
            User.username.label("user__username"),
            User.email.label("user__email"),
        )
        .join(User)
        .where(user_id == Board.user_id, Board.is_deleted.is_(False))
        .order_by(Board.id)
    )
    return to_nested_list(db.execute(query).fetchall())


def fetch_one_(query: Any, db: Session) -> Row:
    row = db.execute(query).fetchone()  # type: ignore
    if not row:
        raise Exception()
    return row


def _fetch_one_or_none(query: Any, db: Session) -> Row | None:
    return db.execute(query).fetchone()


def add_board(name: str, user_id: int, db: Session) -> Row:
    query = insert(Board).values(name=name, user_id=user_id).returning(Board.id, Board.name)
    return fetch_one_(query, db)


def update_board(board_id: int, name: str, user_id: int, db: Session) -> None:
    query = update(Board).where(Board.id == board_id, Board.user_id == user_id).values(name=name)
    db.execute(query)


def delete_board(board_id: int, user_id: int, db: Session) -> None:
    query = (
        update(Board).where(Board.id == board_id, Board.user_id == user_id).values(is_deleted=True).returning(Board.id)
    )
    db.execute(query)


def check_board_exist(board_id: int, user_id: int, db: Session) -> bool:
    query = exists(
        select(Board.is_deleted).where(Board.id == board_id, Board.user_id == user_id, Board.is_deleted.is_(True))
    ).select()
    return db.execute(query).scalar_one()
