from pydantic import BaseModel


class ListSchemaResponse(BaseModel):
    id: int
    name: str
    board_id: int
    ordering: int


class ListResponse(BaseModel):
    list_id: int
    name: str
    board_id: int


class ListCreateSchema(BaseModel):
    name: str


class ListUpdateSchema(BaseModel):
    name: str


class ListOrdering(BaseModel):
    prev_list_ordering: float
