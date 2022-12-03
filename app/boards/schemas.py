from pydantic import BaseModel


class UsersSomeSchema(BaseModel):
    id: int
    username: str
    email: str


class BoardSchema(BaseModel):
    id: int
    name: str
    user: UsersSomeSchema
