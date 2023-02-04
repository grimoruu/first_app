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


class TasksGetSchema(BaseModel):
    list_id: int
    board_id: int


class TaskCreateSchema(BaseModel):
    name: str
    description: str
    list_id: int
    board_id: int


class TaskUpdateSchema(BaseModel):
    task_id: int
    name: str
    description: str
    list_id: int
    board_id: int


class TaskDeleteSchema(BaseModel):
    task_id: int
    list_id: int
    board_id: int
