from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    username: str
    password: str
    email: str


class LoginUserSchema(BaseModel):
    email: str
    password: str


class JWTResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
