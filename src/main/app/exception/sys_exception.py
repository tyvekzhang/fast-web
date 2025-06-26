"""System exception for the application."""

from typing import Optional, Any

from src.main.app.core.exception import CustomException
from src.main.app.enums.sys_error_code import SystemErrorCode


class SystemException(CustomException):
    """Exception class for system-level errors in the application.

    This class should be used for errors related to system operations,
    infrastructure issues, or other technical problems that are not
    directly caused by user input or business logic.
    """

    def __init__(
        self,
        code: SystemErrorCode,
        msg: Optional[Any] = None,
    ):
        super().__init__(code=code, msg=msg)
