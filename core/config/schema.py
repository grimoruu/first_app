from pydantic import BaseModel


class PostgresSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int
    db_name: str
    echo: bool
    autoflush: bool

    def sqlalchemy_database_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class MaxCountOfDigitsSettings(BaseModel):
    max_count: int


class Settings(BaseModel):
    postgres: PostgresSettings
    max_count: MaxCountOfDigitsSettings
