from sqlalchemy.orm import Session

from app.users.dao import get_users
from app.users.schemas import UserSchemaResponse


def get_users_service(db: Session) -> UserSchemaResponse:
    items = get_users(db=db)
    return UserSchemaResponse(items=items)
