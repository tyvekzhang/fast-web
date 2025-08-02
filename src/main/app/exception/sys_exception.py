"""System exception for the application."""

from typing import Optional, Any

from src.main.app.core.exception import HTTPException
from src.main.app.enums.sys_error_code import SystemErrorCode


class SystemException(HTTPException):
    code: SystemErrorCode
    message: Optional[str] = None
    details: Optional[Any] = None
