from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

Items = TypeVar("Items")


class PaginationParams(BaseModel):
    offset: int = 0
    limit: int = 10


class PaginationResponse(GenericModel, Generic[Items]):
    total_count: int
    offset: int
    limit: int
    items: list[Items]
