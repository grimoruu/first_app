from decimal import Decimal

from fastapi import HTTPException, status
from pydantic import BaseModel, root_validator

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

    @root_validator(pre=True)
    def check_patch_values(cls, values: dict) -> dict:
        if not values:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Body can't be empty",
            )
        return values


class ListOrdering(BaseModel):
    prev_list_ordering: Decimal


ListGetDataResponse = PaginationResponse[ListSchemaResponse]
