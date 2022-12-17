from sqlalchemy import select
from sqlalchemy.engine import Row

from db.db import engine
from db.models import User


def get_users() -> list[Row]:
    query = select([User.id, User.username, User.password, User.email]).select_from(User)
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()
