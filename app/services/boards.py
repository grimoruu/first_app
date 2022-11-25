from app.dao.boards import get_boards
from app.schemas.boards import BoardSchema


def get_boards_service():
    rows = get_boards()
    return [BoardSchema(row) for row in rows]