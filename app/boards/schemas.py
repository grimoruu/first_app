from pydantic import BaseModel, EmailStr

from app.lists.schemas import ListResponse
from app.tasks.schemas import TaskResponse


class UsersSomeSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class BoardSchemaResponse(BaseModel):
    id: int
    name: str
    user: UsersSomeSchema


class BoardResponse(BaseModel):
    board_id: int
    name: str


class BoardCreateSchema(BaseModel):
    name: str


class BoardUpdateSchema(BaseModel):
    name: str


class DataSchemaResponse(BaseModel):
    lists: list[ListResponse]
    tasks: list[TaskResponse]
