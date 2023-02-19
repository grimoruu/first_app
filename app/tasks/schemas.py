from pydantic import BaseModel


class TaskSchemaResponse(BaseModel):
    id: int
    name: str
    description: str
    list_id: int
    ordering: float


class TaskResponse(BaseModel):
    task_id: int
    name: str
    description: str
    list_id: int


class TaskCreateSchema(BaseModel):
    name: str
    description: str


class TaskUpdateSchema(BaseModel):
    name: str
    description: str


class TaskOrdering(BaseModel):
    new_list_id: int
    prev_task_ordering: float
