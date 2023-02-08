from sqlalchemy import case, desc, insert, select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

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
    )
    return db.execute(query).fetchall()


def add_list(name: str, board_id: int, ordering: int, user_id: int, db: Session) -> Row | None:
    if check_true_users(board_id=board_id, user_id=user_id, db=db):
        query = (
            insert(List)
            .values(name=name, board_id=board_id, ordering=ordering)
            .returning(List.id, List.name, List.board_id)
        )
        return db.execute(query).fetchone()
    else:
        return None


def update_list(list_id: int, name: str, board_id: int, user_id: int, db: Session) -> Row | None:
    if check_true_users(board_id=board_id, user_id=user_id, db=db):
        query = (
            update(List)
            .where(
                List.id == list_id,
                List.board_id == board_id,
            )
            .values(name=name)
            .returning(List.id, List.name, List.board_id)
        )
        return db.execute(query).fetchone()
    else:
        return None


def delete_list(list_id: int, board_id: int, user_id: int, db: Session) -> Row | None:
    if check_true_users(board_id=board_id, user_id=user_id, db=db):
        query = (
            update(List)
            .where(List.id == list_id, List.board_id == board_id)
            .values(is_deleted=True)
            .returning(List.id, List.name, List.board_id)
        )
        return db.execute(query).fetchone()
    else:
        return None


def get_lists_ordering(board_id: int, db: Session) -> int:
    try:
        query = select(List.ordering).where(List.board_id == board_id).order_by(desc(List.ordering))
        return db.execute(query).fetchall()[0][0] + 1
    except IndexError:
        return 1


def check_true_users(board_id: int, user_id: int, db: Session) -> bool:
    query_select_user = select(Board.user_id).where(Board.id == board_id)
    if db.execute(query_select_user).scalar_one() == user_id:
        return True
    else:
        return False


def swap_lists_ordering(list_: list, board_id: int, user_id: int, db: Session) -> str | None:
    if check_true_users(board_id=board_id, user_id=user_id, db=db):
        query = (
            update(List)
            .values(
                ordering=case(
                    (List.id == list_[0].list_id, list_[1].ordering),
                    (List.id == list_[1].list_id, list_[0].ordering),
                )
            )
            .where(List.id.in_([list_[0].list_id, list_[1].list_id]))
            .returning(List.id)
        )
        result = db.execute(query).fetchall()
        return "lists_swapped"
    else:
        return None
