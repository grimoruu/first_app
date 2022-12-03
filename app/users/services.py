from app.users.dao import get_users
from app.users.schemas import UserSchema


def get_users_service():
    rows = get_users()
    data_on = [UserSchema(**row) for row in rows]
    return data_on


get_users_service()
