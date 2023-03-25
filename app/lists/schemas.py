from decimal import Decimal

from pydantic import BaseModel

from core.pagination.schemas import PaginationResponse


class ListSchemaResponse(BaseModel):
    id: int
    name: str
    description: str | None


class ListCreateSchema(BaseModel):
    name: str
    description: str | None


class ListUpdateSchema(BaseModel):
    name: str | None
    description: str | None


class ListOrdering(BaseModel):
    prev_list_ordering: Decimal


ListGetDataResponse = PaginationResponse[ListSchemaResponse]
