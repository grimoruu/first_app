from fastapi import APIRouter

from app.lists.schemas import ListSchema
from app.lists.services import get_lists_service

router = APIRouter()


@router.get('/lists', response_model=ListSchema)
def lists_list() -> list:
    return get_lists_service()
