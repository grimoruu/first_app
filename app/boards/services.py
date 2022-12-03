from app.boards.dao import get_boards
from app.boards.schemas import BoardSchema, UsersSomeSchema


def get_boards_service():  # -> list[Row]
    rows = get_boards()
    return [
        BoardSchema(
            **row,
            user=UsersSomeSchema(
                id=row.user_id,
                username=row.user_username,
                email=row.user_email,
            )
        )
        for row in rows
    ]
