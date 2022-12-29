from fastapi import APIRouter

from app.users.routes import router as users_router
from app.boards.routes import router as boards_router
from app.lists.routes import router as lists_router
from app.tasks.routes import router as tasks_router
from core.user_util.signup import router as signup_router
from core.user_util.login import router as login_router
from core.user_util.refresh import router as refresh_router
from core.user_util.auth import router as auth_router

router = APIRouter()

router.include_router(users_router, prefix='/users', tags=['users'])
router.include_router(boards_router, prefix='/boards', tags=['board'])
router.include_router(lists_router, prefix='/lists', tags=['list'])
router.include_router(tasks_router, prefix='/tasks', tags=['task'])
router.include_router(signup_router, prefix='/signup', tags=['signup'])
router.include_router(login_router, prefix='/login', tags=['login'])
router.include_router(refresh_router, prefix='/refresh', tags=['refresh'])
router.include_router(auth_router, prefix='/auth', tags=['auth'])