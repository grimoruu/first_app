from fastapi import APIRouter

from app.users.services import get_users_service

router = APIRouter()


@router.get('/users')
def users_list():
    return get_users_service()
