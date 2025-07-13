"""Base exception class for the application."""
from dataclasses import dataclass
from typing import Optional, Any

from src.main.app.core.enums import ExceptionCode


@dataclass
class CustomException(Exception):
    """
    Base exception class for all custom exception in the application.

    Attributes:
        code: The code enum member from BaseErrorCode or its subclasses.
        message: Optional additional message about the error.
        details: Optional extra error details.
    """

    code: ExceptionCode
    message: Optional[str] = None
    details: Optional[Any] = None

    def __post_init__(self):
        if self.message is None:
            self.message = self.code.message
