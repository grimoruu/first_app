from sqlalchemy import select
from sqlalchemy.engine import Row

from db.db import engine
from db.models import Task


def get_tasks() -> list[Row]:
    query = select([Task.id, Task.name, Task.description, Task.list_id, Task.ordering]).select_from(Task)
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()


get_tasks()
