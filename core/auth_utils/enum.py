from datetime import timedelta
from enum import Enum


class ScopeAuthEnum(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class ExpirationTime(Enum):
    ACCESS_TOKEN_EXPIRE_TIME = timedelta(seconds=48 * 60 * 60)  # 48 hours
    REFRESH_TOKEN_EXPIRE_TIME = timedelta(seconds=480 * 60 * 60)  # 480 hours


class SecretKeys(str, Enum):
    JWT_ACCESS_SECRET_KEY = "JWT_ACCESS_SECRET_KEY"
    JWT_REFRESH_SECRET_KEY = "JWT_REFRESH_SECRET_KEY"
