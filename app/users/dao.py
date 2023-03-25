from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.models import User


def get_users(*, db: Session) -> list[Row]:
    query = select(
        User.id,
        User.username,
        User.hashed_password,
        User.email,
    ).select_from(User)
    return db.execute(query).fetchall()
