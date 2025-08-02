"""Auth exception for the application."""

from typing import Optional, Any

from src.main.app.core.exception import HTTPException
from src.main.app.enums.auth_error_code import AuthErrorCode


class AuthException(HTTPException):
    code: AuthErrorCode
    message: Optional[str] = None
    details: Optional[Any] = None
