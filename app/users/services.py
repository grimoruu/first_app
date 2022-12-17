from app.users.dao import get_users
from app.users.schemas import UserSchema


def get_users_service() -> list:
    rows = get_users()
    return [
        UserSchema(**row) for row in rows
    ]
