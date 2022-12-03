from fastapi import APIRouter


from app.boards.services import get_boards_service
from app.lists.services import get_lists_service
from app.tasks.services import get_tasks_service
from app.users.services import get_users_service

# from users.routes import router as user_router
# from boards.routes import router as board_router
# from lists.routes import router as list_router
# from tasks.routes import router as task_router

router = APIRouter()

# router.api_route(user_router)
# router.api_route(board_router)
# router.api_route(list_router)
# router.api_route(task_router)


@router.get("/users")
def get_all_users_api():
    return get_users_service()


@router.get("/boards")
def get_all_boards_api():
    return get_boards_service()


@router.get("/lists")
def get_all_lists_api():
    return get_lists_service()


@router.get("/tasks")
def get_all_task_api():
    return get_tasks_service()
