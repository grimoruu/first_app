from fastapi import APIRouter

from app.auth.routes import router as auth_router
from app.boards.routes import router as boards_router
from app.lists.routes import router as lists_router
from app.tasks.routes import router as tasks_router
from app.users.routes import router as users_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(boards_router, prefix="/boards", tags=["board"])
router.include_router(lists_router, prefix="/lists", tags=["list"])
router.include_router(tasks_router, prefix="/tasks", tags=["task"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
