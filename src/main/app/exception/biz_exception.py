"""Business exception for the application."""

from typing import Optional, Any

from src.main.app.core.enums import ExceptionCode
from src.main.app.core.exception import HTTPException


class BusinessException(HTTPException):
    def __init__(
        self,
        code: ExceptionCode,
        message: Optional[str] = None,
        details: Optional[Any] = None
    ):
        super().__init__(code=code, message=message, details=details)
