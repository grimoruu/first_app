from app.tasks.dao import get_tasks
from app.tasks.schemas import TaskSchema


def get_tasks_service() -> list:
    rows = get_tasks()
    return [
        TaskSchema(**row) for row in rows
    ]
