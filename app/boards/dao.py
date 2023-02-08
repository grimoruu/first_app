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


def add_board(name: str, user_id: int, db: Session) -> Row | None:
    query = insert(Board).values(name=name, user_id=user_id).returning(Board.id, Board.name)
    return db.execute(query).fetchone()


def update_board(board_id: int, name: str, user_id: int, db: Session) -> Row | None:
    query = (
        update(Board)
        .where(Board.id == board_id, Board.user_id == user_id)
        .values(name=name)
        .returning(Board.id, Board.name)
    )
    return db.execute(query).fetchone()


def delete_board(board_id: int, user_id: int, db: Session) -> Row | None:
    query = (
        update(Board)
        .where(Board.id == board_id, Board.user_id == user_id)
        .values(is_deleted=True)
        .returning(Board.id, Board.name)
    )
    return db.execute(query).fetchone()


def check_board_exist(board_id: int, user_id: int, db: Session) -> bool:
    query = exists(
        select(Board.is_deleted).where(Board.id == board_id, Board.user_id == user_id, Board.is_deleted.is_(True))
    ).select()
    return db.execute(query).scalar_one()
