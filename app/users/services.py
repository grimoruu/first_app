from sqlalchemy.orm import Session

from app.users.dao import get_users
from app.users.schemas import UserSchema


def get_users_service(db: Session) -> list[UserSchema]:
    rows = get_users(db)
    return [
        UserSchema(
            **row
         )
        for row in rows
    ]
