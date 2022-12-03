from pydantic import BaseModel


class ListSchema(BaseModel):
    id: int
    name: str
    board_id: int
    ordering: int
