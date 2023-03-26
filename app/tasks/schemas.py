from decimal import Decimal

from fastapi import HTTPException, status
from pydantic import BaseModel, root_validator

from core.pagination.schemas import PaginationResponse


class TaskSchemaResponse(BaseModel):
    name: str
    description: str | None
    list_id: int


class TaskCreateSchema(BaseModel):
    name: str
    description: str | None


class TaskUpdateSchema(BaseModel):
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


class TaskOrderingSchema(BaseModel):
    new_list_id: int
    prev_task_ordering: Decimal


TaskGetDataResponse = PaginationResponse[TaskSchemaResponse]
