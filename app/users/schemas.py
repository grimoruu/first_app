from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: str


class CreateUserSchema(BaseModel):
    username: str
    password: str
    email: str


class LoginUserSchema(BaseModel):
    email: str
    password: str
