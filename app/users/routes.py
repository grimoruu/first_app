from fastapi import APIRouter

from app.users.schemas import UserSchema
from app.users.services import get_users_service

router = APIRouter()


@router.get('/users', response_model=UserSchema)
def users_list() -> list:
    return get_users_service()
