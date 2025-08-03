"""Base error code enumerations for API responses."""

from pydantic import BaseModel


class ExceptionCode(BaseModel):
    """Base class for error code enumerations.

    Provides common interface for all error codes where each enum member is defined as a tuple of
    (code, message). This enables consistent error handling across the codebase.
    """

    code: int
    message: str
