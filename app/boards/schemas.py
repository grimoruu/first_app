from pydantic import BaseModel, EmailStr


class UsersSomeSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class BoardSchema(BaseModel):
    id: int
    name: str
    user: UsersSomeSchema
