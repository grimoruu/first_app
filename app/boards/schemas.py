from pydantic import BaseModel, EmailStr


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
