from fastapi import APIRouter

from app.lists.services import get_lists_service

router = APIRouter()


@router.get('/lists')
def lists_list():
    return get_lists_service()
