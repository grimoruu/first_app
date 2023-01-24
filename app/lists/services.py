from sqlalchemy.orm import Session

from app.lists.dao import get_lists
from app.lists.schemas import ListSchema


def get_lists_service(db: Session) -> list:
    rows = get_lists(db)
    return [
        ListSchema(
            **_
         )
        for _ in rows
    ]
