from sqlalchemy import select
from sqlalchemy.engine import Row
from db.db import engine
from db.models import Board, User


def get_boards() -> list[Row]:
    query = select([User.id, User.username, User.email, Board.id, Board.name]).select_from(Board)
    query = query.join(User)
    with engine.connect() as conn:
        result = conn.execute(query)
        # print(result.fetchall())
        return result.fetchall()


get_boards()
