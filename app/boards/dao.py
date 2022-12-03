from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from core.db_utils import to_nested_list
from db.db import engine
from db.models import Board, User


def get_boards(db: Session) -> list[dict]:
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
    )
    result = db.execute(query)
    return to_nested_list(result.fetchall())



