"""System-related error codes (10000-19999)."""

from src.main.app.core.enums.base_error_code import CustomExceptionCode


class SystemErrorCode(CustomExceptionCode):
    """System-related error codes."""

    INTERNAL_ERROR = (10001, "Internal server error")
