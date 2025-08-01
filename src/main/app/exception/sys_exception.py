"""System exception for the application."""

from typing import Optional, Any

from src.main.app.core.enums import ExceptionCode
from src.main.app.core.exception import HTTPException


class SystemException(HTTPException):
    """Exception class for system-level errors in the application.

    This class should be used for errors related to system operations,
    infrastructure issues, or other technical problems that are not
    directly caused by user input or business logic.
    """

    def __init__(
        self,
        code: ExceptionCode,
        message: Optional[str] = None,
        details: Optional[Any] = None
    ):
        super().__init__(code=code, message=message, details=details)
