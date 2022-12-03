from app.lists.dao import get_lists
from app.lists.schemas import ListSchema


def get_lists_service():
    rows = get_lists()
    print(rows)
    data_on = [ListSchema(**row) for row in rows]
    return data_on

