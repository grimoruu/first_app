from pydantic import BaseModel


class ListSchema(BaseModel):
    id: int
    name: str
    board_id: int
    ordering: int


class ListResponse(BaseModel):
    list_id: int
    board_id: int
    name: str


class ListNameSchema(BaseModel):
    name: str

