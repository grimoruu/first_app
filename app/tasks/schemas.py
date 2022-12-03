from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    name: str
    description: str
    list_id: int
    ordering: str
