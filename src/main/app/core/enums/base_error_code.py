"""Base error code enumerations for API responses."""

from enum import Enum


class ExceptionCode(Enum):
    """Base class for error code enumerations.

    Provides common interface for all error codes where each enum member is defined as a tuple of
    (error_code, error_message). This enables consistent error handling across the codebase.
    """

    @property
    def code(self) -> int:
        """Retrieves the numeric error code."""

        return self.value[0]

    @property
    def message(self) -> str:
        """Retrieves the human-readable error message."""

        return self.value[1]

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
