from sqlalchemy.orm import Session

from app.boards.dao import get_boards
from app.boards.schemas import BoardSchema


def get_boards_service(db: Session) -> list[BoardSchema]:
    rows = get_boards(db)
    return [
        BoardSchema(
            **row
         )
        for row in rows
    ]
