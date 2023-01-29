from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    name: str
    description: str
    list_id: int
    ordering: str


class TaskResponse(BaseModel):
    task_id: int
    name: str
    description: str
    list_id: int


class TaskNameDescSchema(BaseModel):
    name: str
    description: str
