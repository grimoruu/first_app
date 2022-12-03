from fastapi import APIRouter

from app.boards.services import get_boards_service

router = APIRouter()


@router.get('/boards')
def boards_list():
    return get_boards_service()
