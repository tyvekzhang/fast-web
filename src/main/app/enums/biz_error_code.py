"""Business-related error codes (30000-39999)."""

from src.main.app.core.enums.base_error_code import CustomExceptionCode


class BusinessErrorCode(CustomExceptionCode):
    """Business-related error codes."""

    USER_NAME_EXISTS = (30001, "Username already exists")
