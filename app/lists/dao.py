from sqlalchemy import select
from sqlalchemy.engine import Row

from db.db import engine
from db.models import List


def get_lists() -> list[Row]:
    query = select(List.id, List.name, List.board_id, List.ordering).select_from(List)
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()


get_lists()
