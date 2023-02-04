from pydantic import BaseModel


class ListSchema(BaseModel):
    id: int
    name: str
    board_id: int
    ordering: int


class ListResponse(BaseModel):
    list_id: int
    name: str
    board_id: int


class ListsGetSchema(BaseModel):
    board_id: int


class ListCreateSchema(BaseModel):
    name: str
    board_id: int


class ListUpdateSchema(BaseModel):
    list_id: int
    name: str
    board_id: int


class ListDeleteSchema(BaseModel):
    list_id: int
    board_id: int


class ListOrdering(BaseModel):
    list_id: int
    ordering: int


class Ordering(BaseModel):
    board_id: int
    ordering: list[ListOrdering]
