from sqlalchemy.orm import Session

from app.tasks.dao import get_tasks
from app.tasks.schemas import TaskSchema


def get_tasks_service(db: Session) -> list:
    rows = get_tasks(db=db)
    return [
        TaskSchema(
            **_
        )
        for _ in rows
    ]
