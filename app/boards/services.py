from sqlalchemy.orm import Session

from app.boards.dao import add_board, delete_board, get_users_board, update_board
from app.boards.schemas import (
    BoardCreateSchema,
    BoardGetDataResponse,
    BoardsSchemaResponse,
)
from app.lists.services import get_lists_service
from app.tasks.services import get_tasks_service
from core.db_utils import get_count_of_queries, get_paginated, to_nested_list
from core.pagination.schemas import PaginationParams


def get_boards_service(user_id: int, pagination: PaginationParams, *, db: Session) -> BoardsSchemaResponse:
    query = get_users_board(user_id)
    items = to_nested_list(get_paginated(query, pagination.limit, pagination.offset, db=db))
    total_count = get_count_of_queries(query, db=db)
    return BoardsSchemaResponse(total_count=total_count, offset=pagination.offset, limit=pagination.limit, items=items)


def get_boards_data_service(
    board_id: int, user_id: int, pagination: PaginationParams, *, db: Session
) -> BoardGetDataResponse:
    lists = get_lists_service(board_id, user_id, pagination, db=db)
    lists_id = []
    for i in range(len(lists.items)):
        lists_id.append(lists.items[i].id)
    tasks = get_tasks_service(lists_id, board_id, user_id, pagination, db=db)
    return BoardGetDataResponse(lists=lists, tasks=tasks)


def create_board_services(board_create: BoardCreateSchema, user_id: int, *, db: Session) -> None:
    add_board(board_create.name, board_create.description, user_id, db=db)


def update_board_services(board_id: int, board_update: dict, user_id: int, *, db: Session) -> None:
    update_board(board_id, board_update, user_id, db=db)


def delete_board_services(board_id: int, user_id: int, *, db: Session) -> None:
    delete_board(board_id, user_id, db=db)
