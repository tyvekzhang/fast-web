"""Base exception class for the application."""

from typing import Optional, Any

from src.main.app.core.enums import ExceptionCode


class HTTPException(Exception):
    """
    Base exception class for all custom exception in the application.

    Attributes:
        code: The code enum member from BaseErrorCode or its subclasses.
        message: Optional additional message about the error.
        details: Optional extra error details.
    """

    def __init__(
        self, code: ExceptionCode, message: Optional[str] = None, details: Optional[Any] = None
    ):
        """
        Initialize the HTTPException.

        Args:
            code: The error code enum member.
            message: Optional additional message about the error.
            details: Optional extra error details.
        """
        self.code = code
        self.message = message
        self.details = details
        self.__post_init__()

    def __post_init__(self):
        if self.message is None:
            self.message = self.code.message
