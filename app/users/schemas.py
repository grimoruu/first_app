from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    hashed_password: str
    email: str


class UserSchemaResponse(BaseModel):
    items: list[UserSchema]
