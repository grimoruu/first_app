from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.models import List, Task


def get_tasks(db: Session) -> list[Row]:
    query = (
        select(
            Task.id,
            Task.name,
            Task.description,
            Task.list_id,
            Task.ordering,
        )
        .select_from(Task)
        .join(List)
        .where(List.id == Task.list_id)

    )
    result = db.execute(query)
    return result.fetchall()
