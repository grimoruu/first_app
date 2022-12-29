from sqlalchemy import select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.models import User


def get_users(db: Session) -> list[Row]:
    query = (
        select(
            User.id,
            User.username,
            User.password,
            User.email,
        )
        .select_from(User)
    )
    result = db.execute(query)
    return result.fetchall()
