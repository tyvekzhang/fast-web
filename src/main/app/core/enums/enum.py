"""Enumerations module. Contains commonly used enum types for the application."""

from enum import Enum

from src.main.app.core.enums import CustomExceptionCode


class SortEnum(str, Enum):
    """Enumeration for sorting directions."""

    ascending = "asc"
    descending = "desc"


class TokenTypeEnum(str, Enum):
    """Enumeration for token types in authentication."""

    access = "access"
    refresh = "refresh"
    bearer = "Bearer"


class DBTypeEnum(str, Enum):
    """Enumeration for supported database types."""

    PGSQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"


class MediaTypeEnum(str, Enum):
    """Enumeration for media/content types."""

    JSON = ".json"


class CommonErrorCode(CustomExceptionCode):
    """Error codes for core domain."""

    INTERNAL_SERVER_ERROR = (-1, "Internal server exception")
