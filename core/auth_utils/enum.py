from datetime import timedelta
from enum import Enum


class ScopeAuthEnum(str, Enum):
    ACCESS: str = "access_token"
    REFRESH: str = "refresh_token"


class ExpirationTime(Enum):
    ACCESS_TOKEN_EXPIRE_TIME: timedelta = timedelta(seconds=5 * 60)
    REFRESH_TOKEN_EXPIRE_TIME: timedelta = timedelta(seconds=10 * 60)


class SecretKeys(str, Enum):
    JWT_ACCESS_SECRET_KEY: str = "JWT_ACCESS_SECRET_KEY"
    JWT_REFRESH_SECRET_KEY: str = "JWT_REFRESH_SECRET_KEY"
