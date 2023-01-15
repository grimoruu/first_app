from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    hashed_password: str
    email: str
