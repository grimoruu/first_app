from sqlalchemy import select
from sqlalchemy.engine import Row

from db.db import session_local
from db.models import Board


def get_boards():
    query = select(Board.id, Board.name, Board.user_id).select_from(Board)
    rows: list[Row] = something(query)
    return rows