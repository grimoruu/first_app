from fastapi import APIRouter

from app.boards.routes import router as boards_router

router = APIRouter()

router.include_router(boards_router, prefix='/boards', tags=['board'])
