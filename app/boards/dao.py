from sqlalchemy import exists, insert, select, update
from sqlalchemy.orm import Session

from core.db_utils import to_nested_list
from db.models import Board, User


def add_new_board(name: str, user_id: int, db: Session) -> int:
    query = (
        insert(Board)
        .values(
            name=name,
            user_id=user_id
        )
        .returning(Board.id)
    )
    return db.execute(query).scalar_one()


def get_users_board(user_id: int, db: Session) -> list[dict]:
    query = (
        select(
            Board.id,
            Board.name,
            User.id.label("user__id"),
            User.username.label("user__username"),
            User.email.label("user__email"),
        )
        .select_from(Board)
        .join(User)
        .where(user_id == Board.user_id, Board.is_deleted == "false")
    )
    return to_nested_list(db.execute(query).fetchall())


def delete_board(user_id: int, board_id: int, db: Session) -> str:
    query = (
        update(Board)
        .where(Board.id == board_id, Board.user_id == user_id)
        .values(
            is_deleted=True
        )
        .returning(Board.name)
    )
    return db.execute(query).scalar_one()


def check_board_exist(board_id: int, user_id: int, db: Session) -> bool:
    query = (
        exists(
            select(Board.id)
            .where(Board.id == board_id,
                   Board.user_id == user_id,
                   Board.is_deleted == "true")
        )
        .select()
    )
    return db.execute(query).scalar_one()


def update_boards_name(board_id: int, name: str, user_id: int, db: Session) -> str:
    query = (
        update(Board)
        .where(Board.id == board_id, Board.user_id == user_id)
        .values(
            name=name
        )
        .returning(Board.name)
    )
    return db.execute(query).scalar_one()
