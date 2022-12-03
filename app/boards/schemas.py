from pydantic import BaseModel


class UsersSomeSchema(BaseModel):
    id: int
    username: str
    email: str


class BoardSchema(BaseModel):
    id_1: int
    name: str
    user: UsersSomeSchema
