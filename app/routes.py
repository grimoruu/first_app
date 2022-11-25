from fastapi import APIRouter

from app.services.boards import get_boards_service

router = APIRouter()


@router.get("/boards")
def get_all_boards_api():
    return get_boards_service()