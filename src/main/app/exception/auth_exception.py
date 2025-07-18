"""Auth exception for the application."""

from typing import Optional, Any

from src.main.app.core.exception import CustomException
from src.main.app.enums.auth_error_code import AuthErrorCode


class AuthException(CustomException):
    """Exception class for auth-level errors in the application.

    This class should be used for errors related to auth operations,
    infrastructure issues, or other technical problems that are not
    directly caused by user input or business logic.
    """

    def __init__(
        self,
        code: AuthErrorCode,
        msg: Optional[Any] = None,
    ):
        super().__init__(code=code, msg=msg)
