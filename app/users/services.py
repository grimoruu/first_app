from sqlalchemy.orm import Session

from app.users.dao import get_users
from app.users.schemas import UserSchema


def get_users_service(db: Session) -> list[UserSchema]:
    rows: list = get_users(db=db)
    return [UserSchema(**row) for row in rows]
