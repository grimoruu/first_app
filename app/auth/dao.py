from sqlalchemy import exists, insert, select
from sqlalchemy.orm import Session

from app.auth.schemas import CreateUserSchema, LoginUserSchema
from db.models import User


# Checking if a user exists during registration
def check_users_exist(payload: [CreateUserSchema, LoginUserSchema], db: Session) -> bool:
    query = (
        exists(
            select(User.id)
            .where(User.email == payload.email)
        )
        .select()
    )
    return db.execute(query).fetchone()[0]


# Adding a new user
def add_new_user(payload: CreateUserSchema, db: Session) -> id:
    insert_query = (
        insert(User)
        .values(
            username=payload.username,
            hashed_password=payload.password,
            email=payload.email,
            )
    )
    db.execute(insert_query)
    select_query = (
        select(
            User.id
        )
        .select_from(User)
        .where(User.email == payload.email)
    )
    return db.execute(select_query).fetchone()


# Login user
def login_user(payload: LoginUserSchema, db: Session) -> [list]:
    select_query = (
        select(
            User.id,
            User.hashed_password
        )
        .select_from(User)
        .where(User.email == payload.email)
    )
    return db.execute(select_query).fetchone()
