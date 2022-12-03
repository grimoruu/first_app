from sqlalchemy.engine import Row

from app.boards.dao import get_boards
from app.boards.schemas import BoardSchema


def get_boards_service():  #-> list[Row]
    rows = get_boards()
    data_on = [BoardSchema(**row, user=dict(**row)) for row in rows]
    return data_on


get_boards_service()
