from decimal import Decimal

from pydantic import BaseModel

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


class TaskOrderingSchema(BaseModel):
    new_list_id: int
    prev_task_ordering: Decimal


TaskGetDataResponse = PaginationResponse[TaskSchemaResponse]
