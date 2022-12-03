from fastapi import APIRouter

from app.boards.schemas import BoardSchema
from app.boards.services import get_boards_service

router = APIRouter()


@router.get('/boards', response_model=list[BoardSchema])
def boards_list():
    return get_boards_service()
