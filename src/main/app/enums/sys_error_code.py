"""System-related error codes (10000-19999)."""
from http import HTTPStatus

from src.main.app.core.enums.base_error_code import ExceptionCode


class SystemErrorCode:
    """System-related error codes."""

    INTERNAL_ERROR = ExceptionCode(code=HTTPStatus.INTERNAL_SERVER_ERROR, message="Internal server error")
