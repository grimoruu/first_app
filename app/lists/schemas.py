from pydantic import BaseModel


class ListSchemaResponse(BaseModel):
    id: int
    name: str
    board_id: int
    ordering: int
    description: str | None


class ListResponse(BaseModel):
    id: int
    name: str
    description: str | None


class ListCreateSchema(BaseModel):
    name: str


class ListUpdateSchema(BaseModel):
    name: str


class ListOrdering(BaseModel):
    prev_list_ordering: float
