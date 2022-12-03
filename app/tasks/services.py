from app.tasks.dao import get_tasks
from app.tasks.schemas import TaskSchema


def get_tasks_service():
    rows = get_tasks()
    data_on = [TaskSchema(**row) for row in rows]
    return data_on


get_tasks_service()
