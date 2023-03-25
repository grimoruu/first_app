from sqlalchemy import exists, insert, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select

from db.models import Board, User


def get_users_board(user_id: int) -> Select:
    query = (
        select(
            Board.id,
            Board.name,
            Board.description,
            User.id.label("user__id"),
            User.username.label("user__username"),
            User.email.label("user__email"),
        )
        .join(User, Board.user_id == User.id)
        .where(Board.user_id == user_id, Board.is_deleted.is_(False))
        .order_by(Board.id)
    )
    return query


def add_board(name: str, description: str | None, user_id: int, *, db: Session) -> None:
    query = insert(Board).values(name=name, description=description, user_id=user_id)
    db.execute(query)


def update_board(board_id: int, values: dict, user_id: int, *, db: Session) -> None:
    query = update(Board).where(Board.id == board_id, Board.user_id == user_id).values(**values)
    db.execute(query)


def delete_board(board_id: int, user_id: int, *, db: Session) -> None:
    query = update(Board).where(Board.id == board_id, Board.user_id == user_id).values(is_deleted=True)
    db.execute(query)


def check_true_users(board_id: int, user_id: int, *, db: Session) -> bool:
    query = exists(select(Board.id).where(Board.id == board_id, Board.user_id == user_id)).select()
    return db.execute(query).scalar_one()
