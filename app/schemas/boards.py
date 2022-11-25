from pydantic import BaseModel


class BoardSchema(BaseModel):
    id: int
    name: str
    user_id: int