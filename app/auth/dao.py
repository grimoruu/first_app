from typing import Any

from sqlalchemy import exists, insert, select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.models import User


def check_users_exist(email: str, db: Session) -> bool:
    """
    Checking if a user exists during registration
    """
    query = (
        exists(
            select(User.id)
            .where(User.email == email)
        )
        .select()
    )
    return db.execute(query).scalar_one()


def add_new_user(username: str, hashed_password: str, email: str, db: Session) -> int:
    """
    Adding a new user
    """
    query = (
        insert(User)
        .values(
            username=username,
            hashed_password=hashed_password,
            email=email,
        )
        .returning(User.id)
    )
    return db.execute(query).scalar_one()


def login_user(email: str, db: Session) -> Row | Any:
    """
    Login user
    """
    select_query = (
        select(
            User.id,
            User.hashed_password,
        )
        .select_from(User)
        .where(User.email == email))
    return db.execute(select_query).fetchone()
