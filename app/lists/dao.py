from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.models import List


def get_lists(db: Session) -> list[Row]:
    query = (
        select(
            List.id,
            List.name,
            List.board_id,
            List.ordering,
        )
        .select_from(List)
    )
    result = db.execute(query)
    return result.fetchall()
