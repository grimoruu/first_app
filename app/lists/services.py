from app.lists.dao import get_lists
from app.lists.schemas import ListSchema


def get_lists_service() -> list:
    rows = get_lists()
    return [
        ListSchema(**row) for row in rows
    ]


