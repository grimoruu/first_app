from fastapi import HTTPException, status
from pydantic import BaseModel, root_validator

from app.auth.schemas import UsersSomeSchema
from app.lists.schemas import ListGetDataResponse
from app.tasks.schemas import TaskGetDataResponse
from core.pagination.schemas import PaginationResponse


class BoardSchema(BaseModel):
    id: int
    name: str
    description: str | None
    user: UsersSomeSchema


class BoardCreateSchema(BaseModel):
    name: str
    description: str | None


class BoardUpdateSchema(BaseModel):
    name: str | None
    description: str | None

    @root_validator(pre=True)
    def check_patch_values(cls, values: dict) -> dict:
        if not values:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Body can't be empty",
            )
        return values


class BoardGetDataResponse(BaseModel):
    lists: ListGetDataResponse
    tasks: TaskGetDataResponse


BoardsSchemaResponse = PaginationResponse[BoardSchema]
