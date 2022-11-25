from fastapi import APIRouter

from app.services.boards import get_boards_service
from boards.routes import router as board_router

router = APIRouter()

router.api_route(board_router)
router.api_route(board_router)
router.api_route(board_router)
router.api_route(board_router)

@router.get("/boards")
def get_all_boards_api():
    return get_boards_service()