from app.lists.dao import get_lists
from app.lists.schemas import ListSchema


def get_lists_service():
    rows = get_lists()
    data_on = [ListSchema(row) for row in rows]
    return data_on


get_lists_service()
